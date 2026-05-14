---
name: su-draft-template
description: Estructura obligatoria del SU.md draft. Contiene las 9 secciones con markdown completo y anotaciones guía por sección. Invocada por su_synthesizer justo antes de comenzar a redactar, tras completar el protocolo de cuestionamiento activo.
user-invocable: false
---

# Skill: /su-draft-template

Estructura obligatoria del borrador del SU.md. Contiene las 9 secciones con su markdown completo y las anotaciones guía para cada sección. Invocada por `su_synthesizer` justo antes de comenzar a redactar.

---

## Estructura obligatoria del draft (9 secciones)

El draft DEBE contener exactamente estas 9 secciones, en este orden, sin omitir ninguna ni agregar secciones no listadas. Si una sección no tiene información en la entrevista, escribe el contenido que hay y agrega la etiqueta correspondiente — no dejes la sección vacía ni escribas un placeholder genérico como "información pendiente".

```markdown
# SU Draft v{n} — [Nombre del proyecto / descripción breve del problema]

**Versión:** v{n}
**Fecha:** YYYY-MM-DD
**Generado por:** su_synthesizer
**Basado en:** governance/su/su_interview.md (Fase 1 completa, Fase 2 completa)

---

## 1. Contexto del negocio

[Industria, tamaño del área afectada, tiempo de existencia del problema, contexto regulatorio si aplica. Incluir números concretos cuando estén disponibles. Marcar con etiquetas si algo está vago o sin confirmar.]

## 2. Problema central

[El problema en lenguaje de negocio puro. Sin soluciones técnicas, sin jerga de ML/IA. Describir qué está ocurriendo hoy que no debería ocurrir, cuándo empezó y por qué importa resolverlo ahora. Si el stakeholder lo describió como solución técnica, marcar con [ALERTA: PROBLEMA DESCRITO COMO SOLUCIÓN TÉCNICA].]

## 3. Impacto cuantificado

[Impacto económico con número concreto (USD/mes, % de pérdida, horas/semana). Personas afectadas. Impacto en clientes si aplica. Si no hay número concreto, marcar con [AMBIGUO] o [PENDIENTE VALIDACIÓN] — nunca inventar una estimación.]

## 4. Alcance: dentro y fuera

**Dentro del alcance:**
- [Lista explícita de procesos, áreas, sistemas, líneas de negocio que SÍ cubre este proyecto]

**Fuera del alcance:**
- [Lista explícita de lo que NO se toca, con razón cuando fue mencionada]

[Si el stakeholder no definió límites claros, marcar: [ALERTA: ALCANCE SIN LÍMITES EXPLÍCITOS]. Un alcance circular es criterio de rechazo automático.]

## 5. Stakeholders y responsabilidades

| Rol | Nombre | Cargo | Responsabilidad en el proyecto |
|---|---|---|---|
| Aprobador final | [nombre] | [cargo] | Aprueba el documento y el resultado |
| Usuario final | [nombre/grupo] | [cargo] | Usa el sistema día a día |
| Dueño de datos | [nombre] | [cargo] | Autoriza acceso a los datos |
| Resistencias identificadas | [área/persona] | — | [descripción de la resistencia mencionada] |

[Si no hay aprobador nombrado, marcar: [ALERTA: SIN APROBADOR IDENTIFICADO]. Criterio de rechazo automático.]

## 6. Datos disponibles

[Qué datos existen, dónde están guardados (ruta, sistema, formato), años de historia, restricciones de acceso, datos que se sabe que no existen pero serían necesarios. Si los datos son vagos ("tenemos todo en el sistema"), marcar con [AMBIGUO: especificar tablas, fechas y acceso].]

## 7. Criterios de éxito medibles

[Al menos una métrica de negocio con número y plazo. Ejemplos válidos: "reducir tiempo de X a Y en Z meses", "aumentar tasa de X de A% a B%". Ejemplos inválidos: "mejorar la eficiencia", "optimizar el proceso". Si no hay métrica concreta: [ALERTA: SIN MÉTRICA MEDIBLE]. Criterio de rechazo automático.]

## 8. Restricciones y riesgos

**Restricciones confirmadas:**
- Presupuesto: [monto o [AMBIGUO]]
- Plazo: [fecha o [AMBIGUO]]
- Tecnología: [restricciones de plataforma/proveedor o [AMBIGUO]]
- Confidencialidad: [restricciones de acceso a datos o [AMBIGUO]]

**Riesgos identificados:**
- [Riesgo mencionado por el stakeholder + causa raíz si fue explorada]
- [Proyectos similares que fallaron: qué pasó y por qué — si no se exploró la causa raíz: [AMBIGUO: causa raíz no documentada]]

## 9. Intentos previos

[Qué se intentó antes para resolver este problema. Por qué no funcionó o fue insuficiente. Si el stakeholder mencionó intentos sin explicar el fracaso: [PENDIENTE VALIDACIÓN: causa del fracaso no documentada]. Si no hubo intentos previos: documentar explícitamente "No se identificaron intentos previos en la entrevista".]

---

## Resumen de alertas y gaps detectados

[Esta sección es para el orquestador y el evaluador. Lista todas las etiquetas [ALERTA] y [GAP CRÍTICO] del documento, con la sección donde aparecen. Si hay cero alertas, escribir "Sin alertas detectadas".]

| Tipo | Sección | Descripción |
|---|---|---|
| [ALERTA] | 2. Problema central | Problema descrito como solución técnica |
| [GAP CRÍTICO] | 3. Impacto cuantificado | No hay número concreto de impacto económico |

## Cambios respecto a versión anterior

[Solo presente en v2+. Ver instrucciones en sección "Versiones siguientes (v2+)". Omitir completamente en v1.]
```
