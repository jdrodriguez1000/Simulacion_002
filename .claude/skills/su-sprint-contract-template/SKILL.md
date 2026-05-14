---
name: su-sprint-contract-template
description: Template canónico del su_sprint_contract.md. Contiene el objetivo, condiciones de entrada, criterios de terminado, límite de iteraciones, criterios de rechazo automático y tabla de artefactos. Invocado por doc_orchestrator cuando necesita crear governance/su/su_sprint_contract.md.
user-invocable: false
---

# Skill: /su-sprint-contract-template

Template canónico para crear el sprint contract del SU.md. Invocado por `doc_orchestrator` cuando necesita crear `governance/su/su_sprint_contract.md`.

---

## Templates de Sprint Contracts

Plantillas canónicas para crear los sprint contracts de cada documento de gobernanza.
Cada documento tiene su propio sprint contract con criterios específicos.

---

### Template: su_sprint_contract.md

Ruta de destino: `governance/su/su_sprint_contract.md`

```markdown
# Sprint Contract: SU.md

## Objetivo
Producir un su_approved.md que capture el entendimiento compartido del problema
de negocio, aprobado por el stakeholder principal.

## Condiciones de entrada (pre-requisitos)
- [ ] gov_init.py retorno status = "ok" o "warning" recuperado
- [ ] project_state.json tiene active_harness = "governance"
- [ ] Stakeholder principal identificado y disponible para entrevista

## Definicion de terminado (exit criteria)
- [ ] su_interview.md contiene respuestas documentadas de Fase 1 y Fase 2
- [ ] su_draft_v{n}.md tiene score promedio >= 0.8 y ninguna dimension < 0.6
- [ ] Stakeholder reviso y aprobo el draft (registrado en gov_history.log)
- [ ] su_approved.md existe como copia inmutable del draft aprobado
- [ ] gov_state.json refleja su.status = "approved"
- [ ] Commit git con mensaje "SU APPROVED by stakeholder"

## Limite de iteraciones
Maximo cb_threshold ciclos su_synthesizer → su_evaluator (BAJA=2, MEDIA=3, ALTA=4).
Si se alcanza el limite sin aprobacion:
  - doc_orchestrator registra en gov_history.log: "SU escalado a humano tras {cb_threshold} iteraciones"
  - gov_state.json: phase = "human_intervention_required"
  - El harness se detiene hasta que el humano intervenga

## Criterios de rechazo automatico (invalidan el sprint sin contar como iteracion)
- El problema esta descrito en terminos de solucion tecnica, no de negocio
- No hay stakeholder identificado que pueda aprobar
- El alcance no tiene limites claros (todo es "dentro")
- No existe ninguna metrica cuantificable de exito

## Artefactos de entrega obligatorios
| Artefacto            | Ruta                               |
| -------------------- | ---------------------------------- |
| su_interview.md      | governance/su/su_interview.md      |
| su_draft_v{n}.md     | governance/su/su_draft_v{n}.md     |
| su_review.md         | governance/su/su_review.md         |
| su_approved.md       | governance/su/su_approved.md       |
| su_metrics.json      | governance/su/su_metrics.json      |
| su_knowledge_gaps.md | governance/su/su_knowledge_gaps.md |
```
