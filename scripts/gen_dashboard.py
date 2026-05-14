#!/usr/bin/env python3
"""
gen_dashboard.py — Regenera governance/dashboard.html leyendo los artefactos del harness.
Uso: python scripts/gen_dashboard.py
"""

import json
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent


# ── Helpers de lectura ────────────────────────────────────────────────────────

def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default if default is not None else {}


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception:
        return None


# ── Parsers ───────────────────────────────────────────────────────────────────

LOG_RE = re.compile(r'\[(\d{4}-\d{2}-\d{2}[^\]]*)\]\s+(\w+):\s+(.*)')

def parse_log_events(log_text):
    if not log_text:
        return []
    events = []
    for line in log_text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = LOG_RE.match(line)
        if m:
            events.append({
                "timestamp": m.group(1).strip(),
                "agent": m.group(2).strip(),
                "message": m.group(3).strip(),
            })
    return events


def parse_dimension_scores(review_text):
    if not review_text:
        return []
    scores = []
    in_rubric = False
    # Matches rows with 4 cols: | # | Dimension | Score | Observations |
    row_4_re = re.compile(r'^\|\s*\d+\s*\|\s*(.+?)\s*\|\s*(\d+\.?\d*)\s*\|')
    # Fallback: 2-col rows | Dimension | Score |
    row_2_re = re.compile(r'^\|\s*(.+?)\s*\|\s*(\d+\.?\d*)\s*\|')
    SKIP = {"Dimensión", "Dimension", "#", "---", "-"}
    for line in review_text.splitlines():
        if re.search(r'[Rr][uú]brica', line):
            in_rubric = True
            continue
        if not in_rubric:
            continue
        if not line.startswith("|"):
            continue
        m = row_4_re.match(line) or row_2_re.match(line)
        if not m:
            continue
        dim = m.group(1).strip()
        if dim in SKIP or dim.startswith("-"):
            continue
        try:
            score = float(m.group(2))
            if 0.0 <= score <= 1.0:
                scores.append({"dimension": dim, "score": score})
        except ValueError:
            pass
    return scores


def parse_overall_score(review_text):
    if not review_text:
        return None
    m = re.search(r'Score promedio[:\s*]+(\d+\.\d+)', review_text)
    if m:
        return float(m.group(1))
    return None


# ── Constructores de datos ────────────────────────────────────────────────────

DOC_LABELS = {
    "su": "SU.md",
    "brd": "BRD",
    "bdd": "BDD",
    "sad": "SAD",
    "specdd": "specDD",
    "feasibility": "Feasibility",
    "backlog": "Backlog",
}
DOC_ORDER = ["su", "brd", "bdd", "sad", "specdd", "feasibility", "backlog"]

PHASE_LABELS = {
    "fase_0_stakeholders":                     "Fase 0 — Mapeo de stakeholders",
    "fase_1_secciones_1.1_a_1.5":              "Fase 1 — Exploración del problema (1.1–1.5)",
    "fase_2_sponsor_secciones_2.1_a_2.8":      "Fase 2 Sponsor — Confirmación y cierre (2.1–2.8)",
    "fase_2T_tecnico_secciones_2.T.1_a_2.T.3": "Fase 2T Técnico — Restricciones técnicas (2.T.1–2.T.3)",
    "fase_2U_usuario_secciones_2.U.1_a_2.U.2": "Fase 2U Usuario — Flujo y usabilidad (2.U.1–2.U.2)",
    "needs_analysis":                          "Análisis de necesidades (su_needs_analyzer)",
    "synthesis_v1":                            "Síntesis — Draft v1 generado",
    "evaluation_v1":                           "Evaluación automática — Draft v1",
    "audit_v1":                                "Auditoría independiente — Draft v1",
    "stakeholder_approval":                    "Aprobación del stakeholder",
}


def build_pipeline(gov_state):
    documents = {k: v for k, v in gov_state.items() if k in DOC_ORDER}
    pipeline = []
    for doc_id in DOC_ORDER:
        doc = documents.get(doc_id, {"status": "pending"})
        raw_phases = doc.get("completed_phases", [])
        phases = [{"id": p, "label": PHASE_LABELS.get(p, p)} for p in raw_phases]
        pipeline.append({
            "id": doc_id,
            "label": DOC_LABELS[doc_id],
            "status": doc.get("status", "pending"),
            "phase": doc.get("phase", ""),
            "iteration_count": doc.get("iteration_count", 0),
            "complexity": doc.get("complexity", ""),
            "final_score": doc.get("final_score"),
            "approved_date": doc.get("approved_date", ""),
            "gaps_criticos": doc.get("gaps_criticos", 0),
            "gaps_menores": doc.get("gaps_menores", 0),
            "needs_analyzer_confidence": doc.get("needs_analyzer_confidence"),
            "completed_phases": phases,
        })
    return pipeline


def compute_metrics(gov_state, log_events, catalog):
    documents = {k: v for k, v in gov_state.items() if k in DOC_ORDER}
    approved_docs = [d for d in documents.values() if d.get("status") == "approved"]
    non_pending = [d for d in documents.values() if d.get("status") != "pending"]

    computed_vals = {}

    # first_pass_approval_rate
    if non_pending:
        fp = sum(1 for d in non_pending if d.get("iteration_count", 0) == 1 and d.get("status") == "approved")
        computed_vals["first_pass_approval_rate"] = round(fp / len(non_pending), 2)

    # avg_iteration_count
    if approved_docs:
        computed_vals["avg_iteration_count"] = round(
            sum(d.get("iteration_count", 0) for d in approved_docs) / len(approved_docs), 2
        )

    # circuit_breaker_activations
    computed_vals["circuit_breaker_activations"] = sum(
        1 for e in log_events if "CIRCUIT BREAKER activado" in e.get("message", "")
    )

    # human_rejection_count
    computed_vals["human_rejection_count"] = sum(
        1 for e in log_events if "draft rechazado por stakeholder" in e.get("message", "")
    )

    # avg_confidence_at_synthesis
    confidences = [
        d.get("needs_analyzer_confidence")
        for d in approved_docs
        if d.get("needs_analyzer_confidence") is not None
    ]
    if confidences:
        computed_vals["avg_confidence_at_synthesis"] = round(sum(confidences) / len(confidences), 2)

    # Build result list from catalog
    results = []
    for metric in catalog.get("metrics", []):
        mid = metric["id"]
        val = computed_vals.get(mid)
        threshold = metric.get("threshold", {})
        op = threshold.get("operator", "")
        tval = threshold.get("value")

        status = "N/A"
        if val is not None and tval is not None:
            checks = {"lt": val < tval, "gt": val > tval, "lte": val <= tval, "gte": val >= tval, "eq": val == tval}
            status = "OK" if checks.get(op, False) else "ALERTA"

        results.append({
            "id": mid,
            "category": metric.get("category", ""),
            "description": metric.get("description", ""),
            "value": val,
            "threshold_op": op,
            "threshold_val": tval,
            "status": status,
        })
    return results


def build_scores(gov_state, review_text):
    documents = {k: v for k, v in gov_state.items() if k in DOC_ORDER}
    su_doc = documents.get("su", {})
    scores = []

    if su_doc.get("status") == "approved" or su_doc.get("iteration_count", 0) > 0:
        overall = parse_overall_score(review_text)
        dims = parse_dimension_scores(review_text)
        if overall is not None:
            # Threshold: MEDIA → 0.80
            complexity_map = {"low": 0.70, "medium": 0.80, "high": 0.85}
            threshold = complexity_map.get(su_doc.get("complexity", "medium"), 0.80)
            scores.append({
                "doc": "SU.md",
                "versions": [{"version": "v1", "score": overall}],
                "dimensions": dims,
                "threshold": threshold,
            })
    return scores


def build_alerts(failure_modes, pending_changes):
    alerts = []
    for entry in failure_modes.get("failure_log", []):
        alerts.append({
            "type": "failure",
            "title": entry.get("type", "Fallo"),
            "description": entry.get("description", ""),
            "timestamp": entry.get("timestamp", ""),
            "agent": entry.get("agent", ""),
        })
    pc = pending_changes if isinstance(pending_changes, list) else []
    for entry in pc:
        if entry.get("status") == "PENDING_HUMAN_APPROVAL":
            alerts.append({
                "type": "pending_change",
                "title": f"Cambio pendiente: {entry.get('id', '')}",
                "description": entry.get("justification", ""),
                "agent": entry.get("agent_file", ""),
                "timestamp": "",
            })
    return alerts


def build_artifacts(root):
    candidates = [
        ("SU Aprobado", root / "governance/su/su_approved.md"),
        ("SU Entrevista", root / "governance/su/su_interview.md"),
        ("SU Evaluación", root / "governance/su/su_review.md"),
        ("SU Auditoría v1", root / "governance/su/su_audit_v1.md"),
        ("SU Draft v1", root / "governance/su/su_draft_v1.md"),
        ("SU Gaps", root / "governance/su/su_knowledge_gaps.md"),
        ("SU Sprint Contract", root / "governance/su/su_sprint_contract.md"),
    ]
    artifacts = []
    for label, path in candidates:
        content = read_text(path)
        if content is not None:
            artifacts.append({"label": label, "filename": path.name, "content": content})
    return artifacts


# ── Generador HTML ────────────────────────────────────────────────────────────

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Dashboard de Gobernanza — Triple S</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#f1f5f9;color:#1e293b;min-height:100vh;padding:0 0 3rem}
a{color:inherit;text-decoration:none}

/* ── Layout ── */
.page{max-width:960px;margin:0 auto;padding:0 1rem}

/* ── Header ── */
.header{padding:2rem 1rem 1.25rem;max-width:960px;margin:0 auto;display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:1rem}
.header-title h1{font-size:1.55rem;font-weight:700;color:#0f172a}
.header-title p{font-size:0.82rem;color:#64748b;margin-top:.25rem}

/* ── Badge ── */
.badge{display:inline-flex;align-items:center;gap:.4rem;padding:.4rem .95rem;border-radius:9999px;font-size:.75rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.badge .dot{width:7px;height:7px;border-radius:50%;background:currentColor}
.badge-approved{background:#dcfce7;color:#15803d}
.badge-progress{background:#fef9c3;color:#a16207}
.badge-pending{background:#f1f5f9;color:#64748b}
.badge-rejected{background:#fee2e2;color:#b91c1c}

/* ── Tabs ── */
.tabs{max-width:960px;margin:0 auto;padding:0 1rem;display:flex;gap:.25rem;border-bottom:2px solid #e2e8f0;margin-bottom:1.75rem;overflow-x:auto}
.tab-btn{padding:.65rem 1.1rem;border:none;background:transparent;cursor:pointer;font-size:.85rem;font-weight:600;color:#64748b;border-bottom:2px solid transparent;margin-bottom:-2px;white-space:nowrap;transition:color .15s,border-color .15s}
.tab-btn:hover{color:#1e293b}
.tab-btn.active{color:#2563eb;border-bottom-color:#2563eb}

/* ── Tab content ── */
.tab-pane{display:none}
.tab-pane.active{display:block}

/* ── Section title ── */
.section-label{font-size:.72rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:1rem}

/* ── Pipeline ── */
.pipeline-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:.85rem}
.doc-card{background:#fff;border-radius:12px;padding:1.1rem 1rem;box-shadow:0 1px 3px rgba(0,0,0,.07);border-top:3px solid transparent;text-align:center}
.doc-card.status-approved{border-color:#16a34a}
.doc-card.status-in_progress{border-color:#ca8a04}
.doc-card.status-rejected{border-color:#dc2626}
.doc-card.status-pending{border-color:#cbd5e1}
.doc-card .doc-name{font-size:.9rem;font-weight:700;color:#0f172a;margin-bottom:.5rem}
.doc-card .doc-score{font-size:1.4rem;font-weight:700;color:#15803d;line-height:1}
.doc-card .doc-meta{font-size:.7rem;color:#94a3b8;margin-top:.35rem;line-height:1.5}
.doc-card .doc-status-chip{display:inline-block;margin-top:.5rem;font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;padding:.15rem .5rem;border-radius:4px}
.chip-approved{background:#dcfce7;color:#15803d}
.chip-in_progress{background:#fef9c3;color:#a16207}
.chip-rejected{background:#fee2e2;color:#b91c1c}
.chip-pending{background:#f1f5f9;color:#64748b}

/* ── Timeline ── */
.timeline-filters{display:flex;gap:.75rem;margin-bottom:1.25rem;flex-wrap:wrap}
.timeline-filters input,.timeline-filters select{padding:.45rem .75rem;border:1px solid #e2e8f0;border-radius:8px;font-size:.82rem;background:#fff;color:#1e293b;outline:none}
.timeline-filters input:focus,.timeline-filters select:focus{border-color:#93c5fd}
.tl-list{display:flex;flex-direction:column;gap:.6rem}
.tl-row{background:#fff;border-radius:10px;padding:.85rem 1rem;box-shadow:0 1px 2px rgba(0,0,0,.06);display:flex;gap:.9rem;align-items:flex-start}
.tl-ts{font-size:.7rem;color:#94a3b8;white-space:nowrap;padding-top:.1rem;min-width:105px}
.tl-agent-chip{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;padding:.2rem .55rem;border-radius:5px;white-space:nowrap;align-self:flex-start}
.tl-msg{font-size:.84rem;color:#1e293b;line-height:1.5;flex:1}
.tl-empty{font-size:.85rem;color:#94a3b8;text-align:center;padding:2rem}

/* Agent chip colors */
.agent-doc_orchestrator{background:#eff6ff;color:#1d4ed8}
.agent-su_interviewer{background:#f0fdf4;color:#15803d}
.agent-su_synthesizer{background:#fefce8;color:#854d0e}
.agent-su_evaluator{background:#f5f3ff;color:#6d28d9}
.agent-su_needs_analyzer{background:#fff7ed;color:#c2410c}
.agent-doc_auditor{background:#fdf2f8;color:#86198f}
.agent-harness_director{background:#f0f9ff;color:#0369a1}
.agent-default{background:#f1f5f9;color:#475569}

/* ── Scores ── */
.score-doc-block{background:#fff;border-radius:12px;padding:1.25rem 1.5rem;box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:1.25rem}
.score-doc-title{font-size:1rem;font-weight:700;color:#0f172a;margin-bottom:1rem;display:flex;align-items:center;gap:.75rem}
.score-versions{display:flex;gap:.75rem;margin-bottom:1.25rem;flex-wrap:wrap}
.score-version-badge{padding:.35rem .8rem;border-radius:8px;font-size:.82rem;font-weight:700}
.score-version-ok{background:#dcfce7;color:#15803d}
.score-version-fail{background:#fee2e2;color:#b91c1c}
.score-dims{display:flex;flex-direction:column;gap:.55rem}
.score-dim-row{display:flex;align-items:center;gap:.85rem}
.score-dim-name{font-size:.78rem;color:#475569;min-width:180px;flex-shrink:0}
.score-bar-wrap{flex:1;background:#f1f5f9;border-radius:4px;height:10px;position:relative}
.score-bar{height:100%;border-radius:4px;transition:width .3s}
.score-bar-ok{background:#4ade80}
.score-bar-fail{background:#f87171}
.score-bar-threshold{position:absolute;top:-3px;bottom:-3px;width:2px;background:#94a3b8}
.score-dim-val{font-size:.78rem;font-weight:700;min-width:36px;text-align:right}
.score-empty{font-size:.85rem;color:#94a3b8;text-align:center;padding:2rem}

/* ── Metrics ── */
.metrics-table{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.07)}
.metrics-table th{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#94a3b8;padding:.75rem 1rem;text-align:left;border-bottom:1px solid #f1f5f9}
.metrics-table td{padding:.8rem 1rem;border-bottom:1px solid #f8fafc;font-size:.83rem;vertical-align:top}
.metrics-table tr:last-child td{border-bottom:none}
.metrics-table tr:hover td{background:#f8fafc}
.cat-chip{font-size:.62rem;font-weight:700;text-transform:uppercase;padding:.15rem .45rem;border-radius:4px;letter-spacing:.04em}
.cat-eficacia{background:#eff6ff;color:#1d4ed8}
.cat-eficiencia{background:#f0fdf4;color:#15803d}
.cat-robustez{background:#fef2f2;color:#dc2626}
.cat-calidad_ia{background:#faf5ff;color:#7c3aed}
.cat-satisfaccion{background:#fff7ed;color:#c2410c}
.cat-valor_negocio{background:#ecfdf5;color:#059669}
.metric-status{font-size:1rem;text-align:center}
.metric-val{font-weight:700;color:#0f172a}
.metric-val-na{color:#94a3b8}
.threshold-txt{font-size:.75rem;color:#94a3b8}

/* ── Alerts ── */
.alerts-section{margin-bottom:1.5rem}
.alerts-section-title{font-size:.8rem;font-weight:700;color:#475569;margin-bottom:.75rem}
.alert-card{background:#fff;border-radius:10px;padding:1rem 1.25rem;box-shadow:0 1px 2px rgba(0,0,0,.06);margin-bottom:.65rem;border-left:4px solid #f87171}
.alert-card.type-pending_change{border-color:#fb923c}
.alert-card .alert-title{font-size:.88rem;font-weight:700;color:#0f172a;margin-bottom:.3rem}
.alert-card .alert-desc{font-size:.8rem;color:#475569;line-height:1.5}
.alert-card .alert-meta{font-size:.72rem;color:#94a3b8;margin-top:.4rem}
.no-alerts{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:1.5rem;text-align:center;color:#15803d;font-size:.9rem;font-weight:600}

/* ── Artifacts ── */
.artifacts-layout{display:grid;grid-template-columns:200px 1fr;gap:1rem;min-height:400px}
.artifact-list{display:flex;flex-direction:column;gap:.4rem}
.artifact-btn{padding:.6rem .85rem;border:1px solid #e2e8f0;border-radius:8px;background:#fff;cursor:pointer;font-size:.82rem;color:#475569;text-align:left;transition:all .15s;font-weight:500}
.artifact-btn:hover{background:#f8fafc;color:#1e293b}
.artifact-btn.active{background:#eff6ff;border-color:#93c5fd;color:#1d4ed8;font-weight:700}
.artifact-viewer{background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.07);overflow:hidden}
.artifact-header{padding:.75rem 1.25rem;border-bottom:1px solid #f1f5f9;font-size:.8rem;font-weight:700;color:#475569;display:flex;justify-content:space-between;align-items:center}
.artifact-content{padding:1.25rem;overflow:auto;max-height:600px}
.artifact-content pre{font-family:"Menlo","Consolas","Courier New",monospace;font-size:.75rem;line-height:1.6;color:#1e293b;white-space:pre-wrap;word-break:break-word}
.artifact-empty{padding:3rem;text-align:center;color:#94a3b8;font-size:.85rem}

/* ── Phases ── */
.phases-section{margin-top:1.5rem}
.phases-doc-title{font-size:.82rem;font-weight:700;color:#475569;margin-bottom:.6rem;display:flex;align-items:center;gap:.5rem}
.phases-doc-title .phase-doc-badge{font-size:.65rem;font-weight:700;text-transform:uppercase;padding:.15rem .5rem;border-radius:4px}
.phases-list{display:flex;flex-direction:column;gap:.4rem;padding-left:.25rem}
.phase-row{display:flex;align-items:center;gap:.65rem;padding:.45rem .75rem;background:#fff;border-radius:8px;box-shadow:0 1px 2px rgba(0,0,0,.05)}
.phase-icon{font-size:.85rem;flex-shrink:0}
.phase-label{font-size:.82rem;color:#1e293b}

/* ── Footer ── */
footer{max-width:960px;margin:2rem auto 0;padding:0 1rem;display:flex;justify-content:space-between;font-size:.73rem;color:#94a3b8;flex-wrap:wrap;gap:.5rem}
</style>
</head>
<body>

<div class="header">
  <div class="header-title">
    <h1>Dashboard de Gobernanza &mdash; Triple S</h1>
    <p id="header-meta">Generado el __GENERATED_AT__</p>
  </div>
  <span id="global-badge" class="badge badge-pending"><span class="dot"></span> Cargando&hellip;</span>
</div>

<div class="tabs">
  <button class="tab-btn active" onclick="showTab('pipeline')">Pipeline</button>
  <button class="tab-btn" onclick="showTab('timeline')">Timeline</button>
  <button class="tab-btn" onclick="showTab('scores')">Scores</button>
  <button class="tab-btn" onclick="showTab('metrics')">M&eacute;tricas</button>
  <button class="tab-btn" onclick="showTab('alerts')">Alertas <span id="alert-count"></span></button>
  <button class="tab-btn" onclick="showTab('artifacts')">Artefactos</button>
</div>

<div class="page">

  <!-- Tab: Pipeline -->
  <div id="tab-pipeline" class="tab-pane active">
    <p class="section-label">Pipeline de documentos (7 en total)</p>
    <div id="pipeline-grid" class="pipeline-grid"></div>
  </div>

  <!-- Tab: Timeline -->
  <div id="tab-timeline" class="tab-pane">
    <p class="section-label">Historial de eventos</p>
    <div class="timeline-filters">
      <select id="filter-agent" onchange="renderTimeline()">
        <option value="">Todos los agentes</option>
      </select>
      <input id="filter-text" type="text" placeholder="Buscar en mensajes&hellip;" oninput="renderTimeline()"/>
    </div>
    <div id="tl-list" class="tl-list"></div>
  </div>

  <!-- Tab: Scores -->
  <div id="tab-scores" class="tab-pane">
    <p class="section-label">Scores por iteraci&oacute;n y dimensi&oacute;n</p>
    <div id="scores-content"></div>
  </div>

  <!-- Tab: Metrics -->
  <div id="tab-metrics" class="tab-pane">
    <p class="section-label">M&eacute;tricas del harness (cat&aacute;logo de 10)</p>
    <table class="metrics-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Categor&iacute;a</th>
          <th>Descripci&oacute;n</th>
          <th>Valor</th>
          <th>Umbral</th>
          <th style="text-align:center">Estado</th>
        </tr>
      </thead>
      <tbody id="metrics-tbody"></tbody>
    </table>
  </div>

  <!-- Tab: Alerts -->
  <div id="tab-alerts" class="tab-pane">
    <div id="alerts-content"></div>
  </div>

  <!-- Tab: Artifacts -->
  <div id="tab-artifacts" class="tab-pane">
    <p class="section-label">Visor de artefactos</p>
    <div class="artifacts-layout">
      <div id="artifact-list" class="artifact-list"></div>
      <div class="artifact-viewer">
        <div class="artifact-header">
          <span id="artifact-viewer-title">Selecciona un artefacto</span>
          <span id="artifact-viewer-filename" style="font-weight:400;color:#94a3b8"></span>
        </div>
        <div id="artifact-viewer-content" class="artifact-content">
          <div class="artifact-empty">Haz clic en un artefacto para verlo</div>
        </div>
      </div>
    </div>
  </div>

</div><!-- .page -->

<footer>
  <span>Triple S &middot; Documento confidencial</span>
  <span>Dashboard generado por scripts/gen_dashboard.py</span>
</footer>

<script>
const HARNESS_DATA = __DATA_JSON__;

// ── Tab switching ─────────────────────────────────────────────────────────────
function showTab(name) {
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  event.currentTarget.classList.add('active');
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function esc(s) {
  return String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function statusBadgeHtml(status) {
  const map = {
    approved: ['badge-approved','Aprobado'],
    in_progress: ['badge-progress','En progreso'],
    rejected: ['badge-rejected','Rechazado'],
    pending: ['badge-pending','Pendiente'],
  };
  const [cls, label] = map[status] || ['badge-pending', status];
  return `<span class="badge ${cls}"><span class="dot"></span>${label}</span>`;
}

// ── Global badge ──────────────────────────────────────────────────────────────
(function setGlobalBadge() {
  const pipeline = HARNESS_DATA.pipeline || [];
  const total = pipeline.length;
  const approved = pipeline.filter(d => d.status === 'approved').length;
  const inProgress = pipeline.filter(d => d.status === 'in_progress').length;
  const el = document.getElementById('global-badge');
  if (approved === total) {
    el.className = 'badge badge-approved';
    el.innerHTML = '<span class="dot"></span> Completado';
  } else if (inProgress > 0 || approved > 0) {
    el.className = 'badge badge-progress';
    el.innerHTML = `<span class="dot"></span> ${approved}/${total} documentos aprobados`;
  } else {
    el.className = 'badge badge-pending';
    el.innerHTML = `<span class="dot"></span> Iniciando — 0/${total} aprobados`;
  }
})();

// ── Pipeline ──────────────────────────────────────────────────────────────────
(function renderPipeline() {
  const grid = document.getElementById('pipeline-grid');
  const chipMap = {approved:'chip-approved',in_progress:'chip-in_progress',rejected:'chip-rejected',pending:'chip-pending'};
  const labelMap = {approved:'Aprobado',in_progress:'En progreso',rejected:'Rechazado',pending:'Pendiente'};
  grid.innerHTML = (HARNESS_DATA.pipeline || []).map(doc => {
    const scoreHtml = doc.final_score != null
      ? `<div class="doc-score">${doc.final_score.toFixed(2)}</div>`
      : `<div class="doc-score" style="color:#94a3b8;font-size:1rem">&mdash;</div>`;
    const meta = [
      doc.iteration_count > 0 ? `${doc.iteration_count} iter.` : null,
      doc.approved_date ? `${doc.approved_date}` : null,
      doc.complexity ? doc.complexity.toUpperCase() : null,
    ].filter(Boolean).join(' &middot; ');
    return `<div class="doc-card status-${doc.status}">
      <div class="doc-name">${esc(doc.label)}</div>
      ${scoreHtml}
      <div class="doc-meta">${meta || '&mdash;'}</div>
      <span class="doc-status-chip ${chipMap[doc.status]||'chip-pending'}">${labelMap[doc.status]||doc.status}</span>
    </div>`;
  }).join('');
})();

// ── Pipeline phases ───────────────────────────────────────────────────────────
(function renderPhases() {
  const pipeline = HARNESS_DATA.pipeline || [];
  const withPhases = pipeline.filter(d => d.completed_phases && d.completed_phases.length > 0);
  if (!withPhases.length) return;

  const chipMap = {approved:'chip-approved',in_progress:'chip-in_progress',rejected:'chip-rejected',pending:'chip-pending'};
  const labelMap = {approved:'Aprobado',in_progress:'En progreso',rejected:'Rechazado',pending:'Pendiente'};

  const container = document.createElement('div');
  container.className = 'phases-section';

  const sectionLabel = document.createElement('p');
  sectionLabel.className = 'section-label';
  sectionLabel.style.marginTop = '1.75rem';
  sectionLabel.textContent = 'Fases completadas por documento';
  container.appendChild(sectionLabel);

  withPhases.forEach(doc => {
    const titleEl = document.createElement('div');
    titleEl.className = 'phases-doc-title';
    titleEl.innerHTML = `${esc(doc.label)} <span class="phase-doc-badge ${chipMap[doc.status]||'chip-pending'}">${labelMap[doc.status]||doc.status}</span>`;
    container.appendChild(titleEl);

    const list = document.createElement('div');
    list.className = 'phases-list';
    doc.completed_phases.forEach(ph => {
      const row = document.createElement('div');
      row.className = 'phase-row';
      row.innerHTML = `<span class="phase-icon">✅</span><span class="phase-label">${esc(ph.label)}</span>`;
      list.appendChild(row);
    });
    container.appendChild(list);
    container.appendChild(Object.assign(document.createElement('div'), {style:'margin-bottom:1rem'}));
  });

  document.getElementById('tab-pipeline').appendChild(container);
})();

// ── Timeline ──────────────────────────────────────────────────────────────────
(function initTimeline() {
  const sel = document.getElementById('filter-agent');
  const agents = [...new Set((HARNESS_DATA.timeline || []).map(e => e.agent))].sort();
  agents.forEach(a => {
    const opt = document.createElement('option');
    opt.value = a; opt.textContent = a;
    sel.appendChild(opt);
  });
  renderTimeline();
})();

function renderTimeline() {
  const agentFilter = document.getElementById('filter-agent').value;
  const textFilter = document.getElementById('filter-text').value.toLowerCase();
  const events = (HARNESS_DATA.timeline || []).filter(e => {
    if (agentFilter && e.agent !== agentFilter) return false;
    if (textFilter && !e.message.toLowerCase().includes(textFilter)) return false;
    return true;
  });
  const list = document.getElementById('tl-list');
  if (!events.length) {
    list.innerHTML = '<div class="tl-empty">Sin eventos que coincidan con el filtro.</div>';
    return;
  }
  list.innerHTML = events.map(e => {
    const chipClass = `tl-agent-chip agent-${e.agent in {'doc_orchestrator':1,'su_interviewer':1,'su_synthesizer':1,'su_evaluator':1,'su_needs_analyzer':1,'doc_auditor':1,'harness_director':1} ? e.agent : 'default'}`;
    return `<div class="tl-row">
      <span class="tl-ts">${esc(e.timestamp)}</span>
      <span class="${chipClass}">${esc(e.agent)}</span>
      <span class="tl-msg">${esc(e.message)}</span>
    </div>`;
  }).join('');
}

// ── Scores ────────────────────────────────────────────────────────────────────
(function renderScores() {
  const el = document.getElementById('scores-content');
  const scores = HARNESS_DATA.scores || [];
  if (!scores.length) {
    el.innerHTML = '<div class="score-empty">No hay scores disponibles aún. Se generan cuando el primer documento es evaluado.</div>';
    return;
  }
  el.innerHTML = scores.map(doc => {
    const threshold = doc.threshold || 0.80;
    const threshPct = (threshold * 100).toFixed(0);

    const versionsHtml = doc.versions.map(v => {
      const ok = v.score >= threshold;
      return `<div class="score-version-badge ${ok ? 'score-version-ok' : 'score-version-fail'}">${esc(v.version)}: ${v.score.toFixed(2)}</div>`;
    }).join('');

    const dimsHtml = doc.dimensions.map(d => {
      const pct = (d.score * 100).toFixed(0);
      const ok = d.score >= threshold;
      const threshLeft = `calc(${threshPct}% - 1px)`;
      return `<div class="score-dim-row">
        <span class="score-dim-name">${esc(d.dimension)}</span>
        <div class="score-bar-wrap">
          <div class="score-bar ${ok ? 'score-bar-ok' : 'score-bar-fail'}" style="width:${pct}%"></div>
          <div class="score-bar-threshold" style="left:${threshLeft}" title="Umbral ${threshold}"></div>
        </div>
        <span class="score-dim-val" style="color:${ok?'#15803d':'#dc2626'}">${d.score.toFixed(2)}</span>
      </div>`;
    }).join('');

    return `<div class="score-doc-block">
      <div class="score-doc-title">${esc(doc.doc)} <span style="font-size:.75rem;color:#94a3b8;font-weight:500">umbral ${threshold}</span></div>
      <div class="score-versions">${versionsHtml}</div>
      ${doc.dimensions.length ? `<p class="section-label" style="margin-bottom:.75rem">Scores por dimensión</p><div class="score-dims">${dimsHtml}</div>` : ''}
    </div>`;
  }).join('');
})();

// ── Metrics ───────────────────────────────────────────────────────────────────
(function renderMetrics() {
  const tbody = document.getElementById('metrics-tbody');
  const opLabel = {lt:'<', gt:'>', lte:'≤', gte:'≥', eq:'='};
  const statusEmoji = {OK:'✅', ALERTA:'⚠️', 'N/A':'—'};
  tbody.innerHTML = (HARNESS_DATA.metrics || []).map(m => {
    const valHtml = m.value != null
      ? `<span class="metric-val">${m.value}</span>`
      : `<span class="metric-val-na">—</span>`;
    const threshHtml = m.threshold_val != null
      ? `<span class="threshold-txt">${opLabel[m.threshold_op]||m.threshold_op} ${m.threshold_val}</span>`
      : '<span class="threshold-txt">—</span>';
    const catCls = `cat-chip cat-${m.category}`;
    return `<tr>
      <td style="font-size:.75rem;font-weight:700;color:#0f172a;white-space:nowrap">${esc(m.id)}</td>
      <td><span class="${catCls}">${esc(m.category)}</span></td>
      <td style="max-width:280px">${esc(m.description)}</td>
      <td>${valHtml}</td>
      <td>${threshHtml}</td>
      <td class="metric-status">${statusEmoji[m.status]||'—'}</td>
    </tr>`;
  }).join('');
})();

// ── Alerts ────────────────────────────────────────────────────────────────────
(function renderAlerts() {
  const el = document.getElementById('alerts-content');
  const alerts = HARNESS_DATA.alerts || [];
  const alertCount = document.getElementById('alert-count');
  if (alerts.length) {
    alertCount.textContent = `(${alerts.length})`;
    alertCount.style.background = '#fee2e2';
    alertCount.style.color = '#b91c1c';
    alertCount.style.borderRadius = '9999px';
    alertCount.style.padding = '0 .4rem';
    alertCount.style.fontSize = '.65rem';
    alertCount.style.fontWeight = '700';
  }

  if (!alerts.length) {
    el.innerHTML = '<div class="no-alerts">✅ Sin alertas activas &mdash; harness funcionando correctamente</div>';
    return;
  }
  const failures = alerts.filter(a => a.type === 'failure');
  const pending = alerts.filter(a => a.type === 'pending_change');

  let html = '';
  if (failures.length) {
    html += `<div class="alerts-section">
      <p class="alerts-section-title">Fallos del harness (${failures.length})</p>
      ${failures.map(a => `<div class="alert-card type-failure">
        <div class="alert-title">${esc(a.title)}</div>
        ${a.description ? `<div class="alert-desc">${esc(a.description)}</div>` : ''}
        <div class="alert-meta">${a.agent ? esc(a.agent) : ''} ${a.timestamp ? '· ' + esc(a.timestamp) : ''}</div>
      </div>`).join('')}
    </div>`;
  }
  if (pending.length) {
    html += `<div class="alerts-section">
      <p class="alerts-section-title">Cambios de prompt pendientes de aprobación (${pending.length})</p>
      ${pending.map(a => `<div class="alert-card type-pending_change">
        <div class="alert-title">${esc(a.title)}</div>
        ${a.description ? `<div class="alert-desc">${esc(a.description)}</div>` : ''}
        <div class="alert-meta">${a.agent ? esc(a.agent) : ''}</div>
      </div>`).join('')}
    </div>`;
  }
  el.innerHTML = html;
})();

// ── Artifacts ─────────────────────────────────────────────────────────────────
(function renderArtifacts() {
  const artifacts = HARNESS_DATA.artifacts || [];
  const listEl = document.getElementById('artifact-list');
  if (!artifacts.length) {
    listEl.innerHTML = '<div style="font-size:.82rem;color:#94a3b8">Sin artefactos disponibles.</div>';
    return;
  }
  listEl.innerHTML = artifacts.map((a, i) =>
    `<button class="artifact-btn${i===0?' active':''}" onclick="selectArtifact(${i},this)">${esc(a.label)}</button>`
  ).join('');
  if (artifacts.length) selectArtifact(0, listEl.querySelector('.artifact-btn'));
})();

function selectArtifact(idx, btn) {
  document.querySelectorAll('.artifact-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const a = (HARNESS_DATA.artifacts || [])[idx];
  if (!a) return;
  document.getElementById('artifact-viewer-title').textContent = a.label;
  document.getElementById('artifact-viewer-filename').textContent = a.filename;
  document.getElementById('artifact-viewer-content').innerHTML = `<pre>${esc(a.content)}</pre>`;
}
</script>

</body>
</html>
"""


def generate_html(data):
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    html = HTML_TEMPLATE.replace("__GENERATED_AT__", data["generated_at"])
    html = html.replace("__DATA_JSON__", data_json)
    return html


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    root = ROOT

    gov_state      = read_json(root / "governance/gov_state.json")
    log_text       = read_text(root / "governance/gov_history.log") or ""
    catalog        = read_json(root / "gov_metrics_catalog.json", {"metrics": []})
    failure_modes  = read_json(root / "governance/gov_failure_modes.json", {"failure_log": []})
    pending        = read_json(root / "governance/pending_prompt_changes.json", [])
    su_review_text = read_text(root / "governance/su/su_review.md")

    log_events = sorted(parse_log_events(log_text), key=lambda e: e["timestamp"], reverse=True)
    pipeline   = build_pipeline(gov_state)
    metrics    = compute_metrics(gov_state, log_events, catalog)
    scores     = build_scores(gov_state, su_review_text)
    alerts     = build_alerts(failure_modes, pending)
    artifacts  = build_artifacts(root)

    data = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "project": "Triple S",
        "pipeline": pipeline,
        "timeline": log_events,
        "metrics": metrics,
        "scores": scores,
        "alerts": alerts,
        "artifacts": artifacts,
    }

    html = generate_html(data)
    output = root / "governance/dashboard.html"
    output.write_text(html, encoding="utf-8")
    print(f"[gen_dashboard] Dashboard generado: {output}")
    print(f"  Pipeline:   {len(pipeline)} documentos")
    print(f"  Timeline:   {len(log_events)} eventos")
    print(f"  Métricas:   {len(metrics)} ({sum(1 for m in metrics if m['status']=='OK')} OK, {sum(1 for m in metrics if m['status']=='ALERTA')} ALERTA)")
    print(f"  Scores:     {len(scores)} documentos con scores")
    print(f"  Alertas:    {len(alerts)}")
    print(f"  Artefactos: {len(artifacts)}")


if __name__ == "__main__":
    main()
