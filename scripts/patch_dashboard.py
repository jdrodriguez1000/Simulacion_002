#!/usr/bin/env python3
"""Patch governance/dashboard.html: add pipeline progress section."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DASH = ROOT / "governance" / "dashboard.html"

content = DASH.read_text(encoding="utf-8")

# ── 1. CSS ────────────────────────────────────────────────────────────────────
new_css = """
/* ── Pipeline Progress ── */
.prog-section{margin-top:2rem}
.prog-section-title{font-size:.72rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:1rem}
.prog-list{display:flex;flex-direction:column;gap:.65rem}
.prog-item{background:#fff;border-radius:10px;padding:.9rem 1.1rem;box-shadow:0 1px 2px rgba(0,0,0,.06);border-left:4px solid #e2e8f0}
.prog-item.prog-aprobacion{border-color:#10b981}
.prog-item.prog-evaluacion{border-color:#8b5cf6}
.prog-item.prog-sintesis{border-color:#f59e0b}
.prog-item.prog-entrevista{border-color:#3b82f6}
.prog-item.prog-analisis{border-color:#f59e0b}
.prog-item.prog-inicio{border-color:#94a3b8}
.prog-item-header{display:flex;align-items:center;gap:.65rem;margin-bottom:.3rem;flex-wrap:wrap}
.prog-date{font-size:.7rem;color:#94a3b8;font-weight:500}
.prog-phase-tag{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;padding:.15rem .5rem;border-radius:4px}
.ptag-aprobacion{background:#f0fdf4;color:#15803d}
.ptag-evaluacion{background:#f5f3ff;color:#7c3aed}
.ptag-sintesis{background:#fffbeb;color:#b45309}
.ptag-entrevista{background:#eff6ff;color:#2563eb}
.ptag-analisis{background:#fffbeb;color:#b45309}
.ptag-inicio{background:#f1f5f9;color:#64748b}
.prog-msg{font-size:.88rem;color:#1e293b;line-height:1.5}
"""
css_anchor = "</style>"
assert css_anchor in content, "CSS anchor not found"
content = content.replace(css_anchor, new_css + css_anchor, 1)

# ── 2. HTML ───────────────────────────────────────────────────────────────────
html_anchor = '<div id="pipeline-grid" class="pipeline-grid"></div>'
new_html = html_anchor + """
    <div id="pipeline-progress" class="prog-section">
      <p class="prog-section-title">Historial de avance</p>
      <div id="prog-list" class="prog-list"></div>
    </div>"""
assert html_anchor in content, "HTML anchor not found"
content = content.replace(html_anchor, new_html, 1)

# ── 3. JS ─────────────────────────────────────────────────────────────────────
js_anchor = "// ── Timeline ──────────────────────────────────────────────────────────────────"

new_js = r"""// ── Pipeline Progress ─────────────────────────────────────────────────────────
(function renderPipelineProgress() {
  var SKIP = [
    /gov_state\.json\s+actualizado/i,
    /commit git ejecutado/i,
    /lanzando .+ en paralelo/i,
    /iteration_count incrementado/i,
    /needs_analysis completado/i,
    /su_sprint_contract\.md no exist/i,
    /actualizado a su\.status/i,
    /actualizado a phase=/i,
  ];
  function classifyPhase(msg) {
    if (/aprobado por|aprobado\./i.test(msg)) return ['aprobacion','Aprobación'];
    if (/score|evaluad|auditor/i.test(msg)) return ['evaluacion','Evaluación'];
    if (/draft|borrador|síntesis|generado/i.test(msg)) return ['sintesis','Síntesis'];
    if (/fase 1|fase 2|entrevista|secciones capturadas/i.test(msg)) return ['entrevista','Entrevista'];
    if (/complejidad|brecha|análisis/i.test(msg)) return ['analisis','Análisis'];
    return ['inicio','Inicio'];
  }
  function cleanMsg(msg) {
    for (var j = 0; j < SKIP.length; j++) { if (SKIP[j].test(msg)) return null; }
    var t = msg
      .replace(/governance\/su\/\S+/g, '')
      .replace(/governance\/\S+/g, '')
      .replace(/su_draft_v(\d+)\.md/gi, 'primera versión del documento')
      .replace(/su\.md\s*aprobado/gi, 'Documento de Requerimientos aprobado')
      .replace(/su\.md/gi, 'Documento de Requerimientos')
      .replace(/su_review\.md fusionado con secciones de su_evaluator y doc_auditor\./i, 'Revisión y auditoría del documento consolidadas.')
      .replace(/stakeholder/gi, 'cliente')
      .replace(/su_synthesizer|su_evaluator|su_needs_analyzer|doc_auditor|doc_orchestrator|su_interviewer/gi, '')
      .replace(/Gaps?\s+CR[IÍ]TICOS?:\s*\d+,?\s*/gi, '')
      .replace(/Gaps?\s+MENORES?:\s*\d+,?\s*/gi, '')
      .replace(/Gaps?\s+AUSENTES?:\s*\d+,?\s*/gi, '')
      .replace(/Contradicciones?:\s*\d+,?\s*/gi, '')
      .replace(/CRA presentes?:.*?(?=\.|$)/gi, '')
      .replace(/Secciones con marcado:.*?(?=\.|$)/gi, '')
      .replace(/\(etiquetas[^)]*\)/gi, '')
      .replace(/confidence=[\d.]+\s*\([^)]*\)\s*/gi, '')
      .replace(/confidence=[\d.]+\s*/gi, '')
      .replace(/Complexity=\w+\.\s*/gi, '')
      .replace(/Umbral=[\d.]+\.\s*/gi, '')
      .replace(/Acción recomendada:.*$/i, '')
      .replace(/modo P6-2 \w+\s*[—\-]\s*/gi, '')
      .replace(/\(\d+ señales P6-1\)\.?\s*/gi, '')
      .replace(/Señales?:.*$/i, '')
      .replace(/Harness SU\.md completado\./i, 'Proceso de documentación completado.')
      .replace(/Veredicto:\s*/i, '')
      .replace(/Archivo:\s*/gi, '')
      .replace(/Versión:\s*v\d+\.\s*/gi, '')
      .replace(/Alertas detectadas:\s*\d+\.\s*/gi, '')
      .replace(/Sin criterios de rechazo automático\./gi, '')
      .replace(/Score:\s*([\d.]+)/gi, 'Calificación: $1')
      .replace(/Score\s+([\d.]+)\s*>=\s*umbral\s+[\d.]+\s*\(\w+\)\./gi, 'Calificación $1 supera el umbral requerido.')
      .replace(/Avanzando a human_approval\./gi, '')
      .replace(/Plan guardado en gov_progress\.txt\./gi, '')
      .replace(/gov_state\.json\s*indica\s*/gi, '')
      .replace(/su\.phase=\w+/gi, '')
      .replace(/\(\s*Principio\s+\d+\)/gi, '')
      .replace(/Creado antes de iniciar\./gi, '')
      .replace(/\(LISTO\)/gi, '')
      .replace(/\s*\.\s*\./g, '.').replace(/\s{2,}/g, ' ')
      .replace(/^[.,:;—\- ]+/, '').trim();
    if (!t || t.length < 5) return null;
    t = t.charAt(0).toUpperCase() + t.slice(1);
    if (!t.endsWith('.')) t += '.';
    return t;
  }
  function fmtDate(ts) {
    var m = ts.match(/(\d{4})-(\d{2})-(\d{2})(?:\s+(\d{2}):(\d{2}))?/);
    if (!m) return ts;
    var months = ['','ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
    var s = parseInt(m[3]) + ' ' + months[parseInt(m[2])] + ' ' + m[1].slice(2);
    if (m[4]) s += ' · ' + m[4] + ':' + m[5];
    return s;
  }
  var container = document.getElementById('prog-list');
  var events = HARNESS_DATA.timeline || [];
  var items = events.map(function(e) {
    var msg = cleanMsg(e.message);
    if (!msg) return null;
    var ph = classifyPhase(e.message);
    return {date: fmtDate(e.timestamp), msg: msg, phaseKey: ph[0], phaseLabel: ph[1]};
  }).filter(Boolean);
  if (!items.length) {
    container.innerHTML = '<p style="color:#94a3b8;font-size:.85rem;">Sin eventos registrados.</p>';
    return;
  }
  container.innerHTML = items.map(function(it) {
    return '<div class="prog-item prog-' + it.phaseKey + '">'
      + '<div class="prog-item-header">'
      + '<span class="prog-date">' + it.date + '</span>'
      + '<span class="prog-phase-tag ptag-' + it.phaseKey + '">' + it.phaseLabel + '</span>'
      + '</div>'
      + '<div class="prog-msg">' + esc(it.msg) + '</div>'
      + '</div>';
  }).join('');
})();

""" + js_anchor

assert js_anchor in content, f"JS anchor not found: {repr(js_anchor[:60])}"
content = content.replace(js_anchor, new_js, 1)

DASH.write_text(content, encoding="utf-8")
print(f"OK — 3 patches applied to {DASH}")
