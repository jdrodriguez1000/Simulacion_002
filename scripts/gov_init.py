#!/usr/bin/env python3
"""
gov_init.py — Script de inicialización del harness de gobernanza.
Verifica integridad del estado y consistencia con el filesystem antes de
que el doc_orchestrator tome cualquier decisión.

Uso: python scripts/gov_init.py
     Ejecutar desde la raíz del proyecto.

Exit codes:
  0 = ok      (todo coherente, continuar normal)
  1 = warning (inconsistencia recuperable, el orquestador auto-repara)
  2 = critical (JSON corrupto o inconsistencia irrecuperable, detener y escalar)
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# Raíz del proyecto: dos niveles arriba de scripts/
ROOT = Path(__file__).resolve().parent.parent


# ─────────────────────────────────────────────────────────────────────────────
# Helpers de verificación
# ─────────────────────────────────────────────────────────────────────────────

def check_json_valid(path: Path) -> tuple:
    """Verifica que el archivo existe y contiene JSON válido."""
    if not path.exists():
        return False, f"Archivo no encontrado: {path.relative_to(ROOT)}"
    try:
        with open(path, encoding="utf-8") as f:
            json.load(f)
        return True, ""
    except json.JSONDecodeError as e:
        return False, f"JSON inválido en {path.relative_to(ROOT)}: {e}"
    except OSError as e:
        return False, f"No se puede leer {path.relative_to(ROOT)}: {e}"


def check_readable(path: Path) -> tuple:
    """Verifica que el archivo existe y es legible (no necesita ser JSON)."""
    if not path.exists():
        return False, f"Archivo no encontrado: {path.relative_to(ROOT)}"
    try:
        with open(path, encoding="utf-8") as f:
            f.read(1)
        return True, ""
    except OSError as e:
        return False, f"No se puede leer {path.relative_to(ROOT)}: {e}"


def check_git_available() -> tuple:
    """Verifica que git está disponible y el directorio de trabajo es un repo."""
    try:
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=10,
        )
        if result.returncode == 0:
            return True, ""
        return False, f"git status retornó código {result.returncode}: {result.stderr.strip()}"
    except FileNotFoundError:
        return False, "git no está disponible en el PATH"
    except subprocess.TimeoutExpired:
        return False, "git status timeout (>10 s)"


def check_github_remote() -> tuple:
    """Verifica que existe un remoto 'origin' apuntando a GitHub."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=10,
        )
        if result.returncode != 0:
            return False, (
                "No hay remoto 'origin' configurado. "
                "Recomendado: git remote add origin https://github.com/<usuario>/<repo>.git"
            )
        url = result.stdout.strip()
        if "github.com" not in url:
            return False, (
                f"El remoto 'origin' ({url}) no apunta a GitHub. "
                "Se esperaba una URL de github.com."
            )
        return True, url
    except FileNotFoundError:
        return False, "git no está disponible en el PATH"
    except subprocess.TimeoutExpired:
        return False, "git remote get-url origin timeout (>10 s)"


def check_github_remote_reachable() -> tuple:
    """Verifica que el remoto 'origin' es alcanzable (requiere conectividad)."""
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--exit-code", "origin"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=15,
        )
        if result.returncode == 0:
            return True, ""
        return False, (
            f"El remoto 'origin' existe pero no es alcanzable "
            f"(exit code {result.returncode}). Verificar conectividad o credenciales."
        )
    except FileNotFoundError:
        return False, "git no está disponible en el PATH"
    except subprocess.TimeoutExpired:
        return False, "git ls-remote timeout (>15 s) — remoto posiblemente no alcanzable"


def check_phase_filesystem_consistency(gov_state_path: Path) -> tuple:
    """
    Verifica que el phase declarado en gov_state.json corresponde a los archivos
    que deben existir en disco (tabla de consistencia del sprint contract).

    Retorna: (is_consistent: bool, issues: list[str], all_recoverable: bool)
    """
    try:
        with open(gov_state_path, encoding="utf-8") as f:
            state = json.load(f)
    except Exception as e:
        return False, [f"No se pudo leer gov_state.json: {e}"], False

    docs = state.get("documents", {})
    issues = []
    all_recoverable = True
    su_dir = ROOT / "governance" / "su"

    for doc_name, doc_data in docs.items():
        if doc_data.get("status") != "in_progress":
            continue
        phase = doc_data.get("phase", "")

        if doc_name == "su":
            if phase == "interview_phase1":
                # Debe existir su_sprint_contract.md
                if not (su_dir / "su_sprint_contract.md").exists():
                    issues.append(
                        "phase=interview_phase1 pero governance/su/su_sprint_contract.md "
                        "no existe (recuperable: el orquestador puede crearlo)"
                    )
                    # Recuperable: el orquestador ya tiene lógica para crearlo.

            elif phase == "interview_phase2":
                # Debe existir su_interview.md con contenido de Fase 1
                interview = su_dir / "su_interview.md"
                if not interview.exists():
                    issues.append(
                        "phase=interview_phase2 pero governance/su/su_interview.md no existe"
                    )
                    all_recoverable = False
                else:
                    content = interview.read_text(encoding="utf-8")
                    if "## FASE 1" not in content and "1.1" not in content:
                        issues.append(
                            "phase=interview_phase2 pero su_interview.md no contiene "
                            "contenido de Fase 1"
                        )
                        all_recoverable = False

            elif phase in ("synthesizer", "needs_analysis"):
                # Debe existir su_interview.md con Fase 1 Y Fase 2
                interview = su_dir / "su_interview.md"
                if not interview.exists():
                    issues.append(
                        f"phase={phase} pero governance/su/su_interview.md no existe"
                    )
                    all_recoverable = False
                else:
                    content = interview.read_text(encoding="utf-8")
                    has_phase1 = "## FASE 1" in content or "1.1" in content
                    has_phase2 = "## FASE 2" in content or "2.1" in content
                    if not has_phase1:
                        issues.append(
                            f"phase={phase} pero su_interview.md no contiene Fase 1"
                        )
                        all_recoverable = False
                    if not has_phase2:
                        issues.append(
                            f"phase={phase} pero su_interview.md no contiene Fase 2"
                        )
                        all_recoverable = False

            elif phase == "evaluator":
                # Debe existir el draft indicado en current_draft
                current_draft = doc_data.get("current_draft", "")
                if current_draft:
                    draft_path = ROOT / current_draft
                    if not draft_path.exists():
                        issues.append(
                            f"phase=evaluator pero el draft '{current_draft}' indicado "
                            "en gov_state.json no existe en disco"
                        )
                        all_recoverable = False
                else:
                    issues.append(
                        "phase=evaluator pero 'current_draft' no está definido "
                        "en gov_state.json"
                    )
                    all_recoverable = False

            elif phase == "approved":
                # Debe existir su_approved.md
                if not (su_dir / "su_approved.md").exists():
                    issues.append(
                        "phase=approved pero governance/su/su_approved.md no existe"
                    )
                    all_recoverable = False

    return len(issues) == 0, issues, all_recoverable


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    gov_state_path    = ROOT / "governance" / "gov_state.json"
    project_state_path = ROOT / "project_state.json"
    gov_progress_path  = ROOT / "governance" / "gov_progress.txt"
    gov_history_path   = ROOT / "governance" / "gov_history.log"
    gov_su_dir         = ROOT / "governance" / "su"
    output_path        = ROOT / "governance" / "gov_init_report.json"

    checks: dict = {}
    inconsistencies: list = []
    status = "ok"
    recommended_action = "proceed_normal"

    # ── 1. Integridad estructural ─────────────────────────────────────────────

    gov_ok,  gov_err  = check_json_valid(gov_state_path)
    proj_ok, proj_err = check_json_valid(project_state_path)
    prog_ok, prog_err = check_readable(gov_progress_path)
    hist_ok, hist_err = check_readable(gov_history_path)

    checks["state_files_valid"]    = gov_ok and proj_ok
    checks["state_files_readable"] = prog_ok and hist_ok

    if not gov_ok:
        inconsistencies.append(gov_err)
        status = "critical"
        recommended_action = "manual_repair_required"

    if not proj_ok:
        inconsistencies.append(proj_err)
        status = "critical"
        recommended_action = "manual_repair_required"

    if not prog_ok:
        inconsistencies.append(prog_err)
        if status != "critical":
            status = "warning"
            recommended_action = "auto_repair_and_continue"

    if not hist_ok:
        inconsistencies.append(hist_err)
        if status != "critical":
            status = "warning"
            recommended_action = "auto_repair_and_continue"

    # ── 2. Sanidad del ambiente ───────────────────────────────────────────────

    git_ok, git_err = check_git_available()
    checks["git_available"] = git_ok
    if not git_ok:
        inconsistencies.append(git_err)
        if status != "critical":
            status = "warning"
            recommended_action = "auto_repair_and_continue"

    su_dir_ok = gov_su_dir.exists() and gov_su_dir.is_dir()
    checks["governance_su_dir_exists"] = su_dir_ok
    if not su_dir_ok:
        inconsistencies.append("Directorio governance/su/ no existe")
        if status != "critical":
            status = "warning"
            recommended_action = "auto_repair_and_continue"

    sprint_contract_path = gov_su_dir / "su_sprint_contract.md"
    sprint_ok = sprint_contract_path.exists()
    checks["sprint_contract_exists"] = sprint_ok
    if not sprint_ok:
        inconsistencies.append(
            "governance/su/su_sprint_contract.md no existe (recuperable)"
        )
        if status != "critical":
            status = "warning"
            recommended_action = "auto_repair_and_continue"

    # ── 3. Remoto GitHub ─────────────────────────────────────────────────────
    #    Nunca escala a critical — un repo puramente local sigue siendo funcional.

    remote_ok, remote_info = check_github_remote()
    checks["github_remote_configured"] = remote_ok
    if not remote_ok:
        inconsistencies.append(remote_info)
        if status != "critical":
            status = "warning"
            recommended_action = "auto_repair_and_continue"
    else:
        reachable_ok, reachable_err = check_github_remote_reachable()
        checks["github_remote_reachable"] = reachable_ok
        if not reachable_ok:
            inconsistencies.append(reachable_err)
            if status != "critical":
                status = "warning"
                recommended_action = "auto_repair_and_continue"

    # ── 4. Consistencia fase → filesystem ────────────────────────────────────
    #    Solo se evalúa si gov_state.json era JSON válido.

    if gov_ok:
        fs_ok, fs_issues, fs_recoverable = check_phase_filesystem_consistency(
            gov_state_path
        )
        checks["filesystem_consistent"] = fs_ok
        if not fs_ok:
            inconsistencies.extend(fs_issues)
            if not fs_recoverable:
                status = "critical"
                recommended_action = "manual_repair_required"
            elif status != "critical":
                status = "warning"
                recommended_action = "auto_repair_and_continue"
    else:
        checks["filesystem_consistent"] = False

    # ── 5. Escribir gov_init_report.json ─────────────────────────────────────

    report = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "checks": checks,
        "inconsistencies": inconsistencies,
        "recommended_action": recommended_action,
    }

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"ERROR: No se pudo escribir gov_init_report.json: {e}", file=sys.stderr)
        return 2

    # ── 6. Imprimir resumen en stdout ─────────────────────────────────────────

    print(f"[gov_init] Status: {status.upper()}")
    if inconsistencies:
        for issue in inconsistencies:
            print(f"  ISSUE: {issue}")
    else:
        print("  Todas las verificaciones pasaron sin problemas.")
    print(f"[gov_init] Reporte escrito en governance/gov_init_report.json")

    # ── 7. Exit code ─────────────────────────────────────────────────────────

    if status == "ok":
        return 0
    elif status == "warning":
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
