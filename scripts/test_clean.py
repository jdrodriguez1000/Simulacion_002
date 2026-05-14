#!/usr/bin/env python3
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

SKIP = [
    re.compile(r'^gov_state\.json', re.I),
    re.compile(r'commit git ejecutado', re.I),
    re.compile(r'lanzando .+ en paralelo', re.I),
    re.compile(r'iteration_count incrementado', re.I),
    re.compile(r'needs_analysis completado', re.I),
    re.compile(r'su_sprint_contract\.md no exist', re.I),
    re.compile(r'^sesión iniciada\.', re.I),
]

def clean(msg):
    for r in SKIP:
        if r.search(msg): return None
    t = msg
    t = re.sub(r'governance/su/\S+', '', t)
    t = re.sub(r'governance/\S+', '', t)
    t = re.sub(r'su_draft_v(\d+)\.md', r'primera versión del documento', t, flags=re.I)
    t = re.sub(r'su\.md\s*aprobado', 'Documento de Requerimientos aprobado', t, flags=re.I)
    t = re.sub(r'su\.md', 'Documento de Requerimientos', t, flags=re.I)
    t = re.sub(r'su_review\.md fusionado con secciones de su_evaluator y doc_auditor\.', 'Revisión y auditoría del documento consolidadas.', t, flags=re.I)
    t = re.sub(r'stakeholder', 'cliente', t, flags=re.I)
    t = re.sub(r'su_synthesizer|su_evaluator|su_needs_analyzer|doc_auditor|doc_orchestrator|su_interviewer', '', t, flags=re.I)
    t = re.sub(r'Gaps?\s+CR[IÍ]TICOS?:\s*\d+,?\s*', '', t, flags=re.I)
    t = re.sub(r'Gaps?\s+MENORES?:\s*\d+,?\s*', '', t, flags=re.I)
    t = re.sub(r'Gaps?\s+AUSENTES?:\s*\d+,?\s*', '', t, flags=re.I)
    t = re.sub(r'Contradicciones?:\s*\d+,?\s*', '', t, flags=re.I)
    t = re.sub(r'CRA presentes?:.*?(?=\.|$)', '', t, flags=re.I)
    t = re.sub(r'Secciones con marcado:.*?(?=\.|$)', '', t, flags=re.I)
    t = re.sub(r'\(etiquetas[^)]*\)', '', t, flags=re.I)
    t = re.sub(r'confidence_score=[\d.]+\s*\([^)]*\)\s*', '', t, flags=re.I)
    t = re.sub(r'confidence_score=[\d.]+\s*', '', t, flags=re.I)
    t = re.sub(r'confidence=[\d.]+\s*\([^)]*\)\s*', '', t, flags=re.I)
    t = re.sub(r'confidence=[\d.]+\s*', '', t, flags=re.I)
    t = re.sub(r'\s*gov_state\.json\s+actualizado.*$', '', t, flags=re.I)
    t = re.sub(r'\bdraft\s+v(\d+)\b', r'versión \1 del documento', t, flags=re.I)
    t = re.sub(r'Gaps:\s*\d+\s*CR[ÍI]TICOS?,\s*\d+\s*MENORES?,\s*\d+\s*AUSENTES?\.?\s*', '', t, flags=re.I)
    t = re.sub(r'Complexity=\w+\.\s*', '', t, flags=re.I)
    t = re.sub(r'Umbral=[\d.]+\.\s*', '', t, flags=re.I)
    t = re.sub(r'Acción recomendada:.*$', '', t, flags=re.I)
    t = re.sub(r'modo P6-2 \w+\s*[—-]\s*', '', t, flags=re.I)
    t = re.sub(r'\(\d+ señales P6-1\)\.?\s*', '', t, flags=re.I)
    t = re.sub(r'Señales?:.*$', '', t, flags=re.I)
    t = re.sub(r'Harness SU\.md completado\.', 'Proceso de documentación completado.', t, flags=re.I)
    t = re.sub(r'Veredicto:\s*', '', t, flags=re.I)
    t = re.sub(r'Archivo:\s*', '', t, flags=re.I)
    t = re.sub(r'Versión:\s*v\d+\.\s*', '', t, flags=re.I)
    t = re.sub(r'Alertas detectadas:\s*\d+\.\s*', '', t, flags=re.I)
    t = re.sub(r'Sin criterios de rechazo automático\.', '', t, flags=re.I)
    t = re.sub(r'Score:\s*([\d.]+)', r'Calificación: \1', t, flags=re.I)
    t = re.sub(r'Score\s+([\d.]+)\s*>=\s*umbral\s+[\d.]+\s*\(\w+\)\.', r'Calificación \1 supera el umbral requerido.', t, flags=re.I)
    t = re.sub(r'Avanzando a human_approval\.', '', t, flags=re.I)
    t = re.sub(r'Plan guardado en gov_progress\.txt\.', '', t, flags=re.I)
    t = re.sub(r'gov_state\.json\s*indica\s*', '', t, flags=re.I)
    t = re.sub(r'su\.phase=\w+', '', t, flags=re.I)
    t = re.sub(r'\(\s*Principio\s+\d+\)', '', t, flags=re.I)
    t = re.sub(r'Creado antes de iniciar\.', '', t, flags=re.I)
    t = re.sub(r'\(LISTO\)', '', t, flags=re.I)
    t = re.sub(r'(\.\s*)+\.', '.', t)
    t = re.sub(r'\s+\.', '.', t)
    t = re.sub(r'\s{2,}', ' ', t)
    t = re.sub(r'^[.,:;—\- ]+', '', t).strip()
    if not t or len(t) < 5: return None
    t = t[0].upper() + t[1:]
    if not t.endswith('.'): t += '.'
    return t

timeline = [
    ('2026-05-08 17:45', "commit git ejecutado: 'SU APPROVED by stakeholder'. Harness SU.md completado."),
    ('2026-05-08 17:45', 'SU.md aprobado por stakeholder. Correcciones incorporadas: tasa línea 1 corregida a 5.1%, plazo corregido a agosto 2026. gov_state.json actualizado a su.status=approved.'),
    ('2026-05-08 17:32', 'su_review.md fusionado con secciones de su_evaluator y doc_auditor. Score 0.84 >= umbral 0.80 (MEDIA). Avanzando a human_approval.'),
    ('2026-05-08 17:30', 'draft v1 evaluado. Score: 0.84. Veredicto: APROBADO. Gaps críticos: 0. Archivo: governance/su/su_review.md'),
    ('2026-05-08 00:00', 'auditoría v1 completada. Gaps CRITICOS: 2, Gaps MENORES: 4, Contradicciones: 2, CRA presentes: 0 de 4. Archivo: governance/su/su_audit_v1.md'),
    ('2026-05-08 17:16', 'lanzando su_evaluator y doc_auditor en paralelo para su_draft_v1.md.'),
    ('2026-05-08 17:16', 'gov_state.json actualizado a phase=evaluator, current_draft=su_draft_v1.md.'),
    ('2026-05-08 17:15', 'su_draft_v1.md generado. Versión: v1. Alertas detectadas: 0. Gaps críticos: 0. Secciones con marcado: 7 (etiquetas PENDIENTE VALIDACIÓN x3, PENDIENTE DE CLARIFICACIÓN x2, AMBIGUO x4). Sin criterios de rechazo automático.'),
    ('2026-05-08 17:01', 'iteration_count incrementado a 1. Invocando su_synthesizer para generar su_draft_v1.md.'),
    ('2026-05-08 17:01', 'needs_analysis completado. confidence=0.90 (LISTO). Gaps: 0 CRITICOS, 2 MENORES, 0 AUSENTES.'),
    ('2026-05-08 17:00', 'análisis completado. Complexity=medium. confidence_score=0.90 (LISTO). Gaps: 0 CRITICOS, 2 MENORES, 0 AUSENTES. Umbral=0.80. Acción recomendada: invocar su_synthesizer directamente.'),
    ('2026-05-08 16:36', 'gov_state.json actualizado a phase=needs_analysis.'),
    ('2026-05-08 16:35', 'Fase 2 completada — modo P6-2 MEDIA — 8 secciones capturadas.'),
    ('2026-05-08 15:46', 'complejidad clasificada como MEDIA (3 señales P6-1). Señales: industria_regulada, alcance_multi_area, proyecto_previo_fallido. gov_state.json actualizado.'),
    ('2026-05-08 15:46', 'gov_state.json actualizado a phase=interview_phase2.'),
    ('2026-05-08 15:45', 'Fase 1 completada — 5 secciones capturadas.'),
    ('2026-05-08 00:00', 'su_sprint_contract.md no existía. Creado antes de iniciar (Principio 5).'),
    ('2026-05-08 00:00', 'sesión iniciada. gov_state.json indica su.phase=interview_phase1. Plan guardado en gov_progress.txt.'),
]

for ts, msg in timeline:
    result = clean(msg)
    if result:
        print(f'[{ts}] {result}')
    else:
        print(f'[{ts}] --- FILTRADO ---')
