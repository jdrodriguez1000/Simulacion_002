#!/usr/bin/env python3
"""
check_harness_integrity.py — Verifica integridad de los artefactos del harness de gobernanza.

Checks:
  1. governance/gov_state.json     — JSON válido, campos harness/documents/last_updated presentes
  2. gov_failure_modes.json        — JSON válido, campo failure_log es array
  3. gov_metrics_catalog.json      — JSON válido, campo metrics es array con id/formula/threshold
  4. governance/gov_history.log    — cada línea cumple [YYYY-MM-DD HH:MM] agente: mensaje
  5. Archivos *_approved.md        — contienen todas las secciones H2 requeridas

Salida: siempre exit 0 (modo alerta, no bloqueo). Imprime OK o WARN por check.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_SU_H2 = [
    "Contexto del negocio",
    "Problema central",
    "Impacto cuantificado",
    "Alcance",
    "Stakeholders",
    "Datos disponibles",
    "Criterios de",
    "Restricciones",
    "Intentos previos",
]

LOG_LINE_PATTERN = re.compile(
    r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] .+: .+"
)

warnings = []


def ok(label: str) -> None:
    print(f"  OK    {label}")


def warn(label: str, detail: str) -> None:
    print(f"  WARN  {label} — {detail}")
    warnings.append(f"{label}: {detail}")


# ─────────────────────────────────────────────────────────────────────────────
# Check 1 — governance/gov_state.json
# ─────────────────────────────────────────────────────────────────────────────

def check_gov_state() -> None:
    label = "governance/gov_state.json"
    path = ROOT / "governance" / "gov_state.json"
    if not path.exists():
        warn(label, "archivo no encontrado")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        warn(label, f"JSON inválido: {e}")
        return
    missing = [f for f in ("harness", "documents", "last_updated") if f not in data]
    if missing:
        warn(label, f"campos faltantes: {missing}")
    else:
        ok(label)


# ─────────────────────────────────────────────────────────────────────────────
# Check 2 — governance/gov_failure_modes.json
# ─────────────────────────────────────────────────────────────────────────────

def check_failure_modes() -> None:
    label = "governance/gov_failure_modes.json"
    path = ROOT / "governance" / "gov_failure_modes.json"
    if not path.exists():
        warn(label, "archivo no encontrado")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        warn(label, f"JSON inválido: {e}")
        return
    if "failure_log" not in data:
        warn(label, "campo 'failure_log' faltante")
    elif not isinstance(data["failure_log"], list):
        warn(label, f"'failure_log' debe ser array, es {type(data['failure_log']).__name__}")
    else:
        ok(label)


# ─────────────────────────────────────────────────────────────────────────────
# Check 3 — gov_metrics_catalog.json
# ─────────────────────────────────────────────────────────────────────────────

def check_metrics_catalog() -> None:
    label = "gov_metrics_catalog.json"
    path = ROOT / "gov_metrics_catalog.json"
    if not path.exists():
        warn(label, "archivo no encontrado")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        warn(label, f"JSON inválido: {e}")
        return
    if "metrics" not in data:
        warn(label, "campo 'metrics' faltante")
        return
    if not isinstance(data["metrics"], list):
        warn(label, f"'metrics' debe ser array, es {type(data['metrics']).__name__}")
        return
    bad_entries = []
    for i, entry in enumerate(data["metrics"]):
        missing = [f for f in ("id", "formula", "threshold") if f not in entry]
        if missing:
            bad_entries.append(f"entrada[{i}] falta: {missing}")
    if bad_entries:
        warn(label, "; ".join(bad_entries))
    else:
        ok(label)


# ─────────────────────────────────────────────────────────────────────────────
# Check 4 — governance/gov_history.log
# ─────────────────────────────────────────────────────────────────────────────

def check_history_log() -> None:
    label = "governance/gov_history.log"
    path = ROOT / "governance" / "gov_history.log"
    if not path.exists():
        warn(label, "archivo no encontrado")
        return
    bad_lines = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if not LOG_LINE_PATTERN.match(line):
            bad_lines.append(f"línea {i}: {line[:60]!r}")
        if len(bad_lines) >= 5:
            bad_lines.append("... (se muestran solo los primeros 5)")
            break
    if bad_lines:
        warn(label, "líneas con formato incorrecto:\n    " + "\n    ".join(bad_lines))
    else:
        ok(label)


# ─────────────────────────────────────────────────────────────────────────────
# Check 5 — archivos *_approved.md
# ─────────────────────────────────────────────────────────────────────────────

def check_approved_docs() -> None:
    approved_files = list(ROOT.rglob("*_approved.md"))
    if not approved_files:
        ok("*_approved.md (ninguno encontrado — harness en curso)")
        return

    required_by_prefix = {
        "su": REQUIRED_SU_H2,
    }

    for path in approved_files:
        label = str(path.relative_to(ROOT))
        prefix = path.stem.replace("_approved", "")
        required = required_by_prefix.get(prefix)
        if required is None:
            ok(f"{label} (secciones requeridas no definidas aún para '{prefix}')")
            continue
        content = path.read_text(encoding="utf-8")
        h2_sections = re.findall(r"^## (.+)", content, re.MULTILINE)
        missing = [s for s in required if not any(s.lower() in h.lower() for h in h2_sections)]
        if missing:
            warn(label, f"secciones H2 faltantes: {missing}")
        else:
            ok(label)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("-- Harness Integrity Check --")
    check_gov_state()
    check_failure_modes()
    check_metrics_catalog()
    check_history_log()
    check_approved_docs()
    print()
    if warnings:
        print(f"Resultado: {len(warnings)} WARN(s) detectados.")
        for w in warnings:
            print(f"  • {w}")
    else:
        print("Resultado: todos los checks OK.")
    # Siempre exit 0 — modo alerta, no bloqueo
    sys.exit(0)


if __name__ == "__main__":
    main()
