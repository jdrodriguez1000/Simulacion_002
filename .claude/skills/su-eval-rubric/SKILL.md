---
name: su-eval-rubric
description: Rúbrica de evaluación para el SU.md. Carga el protocolo de 10 pruebas de estrés, los 3 ejemplos de calibración few-shot (A, B, C) y las 8 dimensiones con árboles de decisión y tablas de scoring (0.0–1.0). Invocada por su_evaluator al inicio del Paso 2.
user-invocable: false
---

# Skill: /su-eval-rubric

Rúbrica de evaluación para el SU.md. Contiene el protocolo de 10 pruebas de estrés, los 3 ejemplos de calibración few-shot y las 8 dimensiones con árboles de decisión y tablas de scoring. Invocada por `su_evaluator` al inicio del Paso 2.

---

## Protocolo de pruebas de estrés (ejecutar ANTES de asignar scores)

Antes de completar la rúbrica, somete el draft a estas 10 pruebas de estrés. Documenta el resultado de cada prueba en tu evaluación:

1. **Prueba de la pregunta "¿y eso qué significa exactamente?"**
   Para cada afirmación de negocio clave, pregúntate: "¿Podría un externo ejecutar este proyecto con solo leer este documento?" Si hay ambigüedad que requeriría una pregunta de seguimiento, es un gap.

2. **Prueba de la métrica de éxito.**
   ¿El criterio de éxito es verificable por un tercero sin acceso al stakeholder? "Mejorar la satisfacción del cliente" no pasa. "Reducir el churn de 15% a 8% en 6 meses medido por el sistema CRM" sí pasa.

3. **Prueba del alcance negativo.**
   ¿Está documentado explícitamente lo que está FUERA del alcance? Un documento que solo define el "dentro" pero no el "fuera" tiene alcance abierto. Un alcance abierto es un riesgo de scope creep garantizado.

4. **Prueba del aprobador real.**
   ¿Hay un nombre y cargo específicos del aprobador del proyecto? ¿Queda claro quién firma el documento final? Si el aprobador es "el equipo" o "la dirección", no hay aprobador real.

5. **Prueba de los datos existentes.**
   ¿Está documentado dónde están los datos, desde cuándo existen, quién tiene acceso y si hay restricciones? "Tenemos datos en el sistema" sin especificar no es suficiente para el BRD ni el specDD.

6. **Prueba de contradicciones internas.**
   Lee el documento de inicio a fin buscando afirmaciones que se contradigan entre secciones. Ejemplo: "no hay presupuesto definido" en la sección de restricciones vs. "el presupuesto es USD 40,000" en el contexto. Cada contradicción no resuelta es un fallo de consistencia interna.

7. **Prueba de las etiquetas del synthesizer.**
   El synthesizer puede haber marcado alertas con `[ALERTA]`, `[GAP CRÍTICO]`, `[AMBIGUO]`, `[CONTRADICCIÓN]` o `[PENDIENTE VALIDACIÓN]`. ¿Hay alguna de estas etiquetas en el draft? Si existe al menos un `[ALERTA]` o `[GAP CRÍTICO]`, verifica que el score en la dimensión correspondiente lo refleje. No ignores las etiquetas del synthesizer.

8. **Prueba del "¿por qué ahora?"**
   ¿Está documentado por qué este problema es urgente en este momento? Si el problema "existe desde hace 5 años" pero no hay contexto de por qué se resuelve ahora, hay un vacío de motivación que generará resistencia en los stakeholders.

9. **Prueba de los intentos previos.**
   ¿Se documentaron intentos previos de resolver el problema? Si no hay mención de intentos previos (o de su inexistencia), es posible que el draft esté ignorando lecciones aprendidas. Un proyecto que repite un error anterior es un riesgo operacional.

10. **Prueba de los riesgos silenciados.**
    ¿Los riesgos documentados son los riesgos reales? Un riesgo que "ya fue manejado" sin documentar cómo es un riesgo activo. Los riesgos deben tener mitigación o reconocimiento explícito, no desaparecer del documento.

---

## Calibración few-shot — Referencia obligatoria

Antes de evaluar cualquier draft real, lee estos tres ejemplos. Tu scoring debe ser **consistente con estos ejemplos**. Si tu score difiere en más de ±0.10 del score de referencia para un draft equivalente, revisa tu razonamiento.

### Ejemplo A — Draft deficiente (score promedio de referencia: 0.26)

**Fragmento del draft evaluado:**
> "El proyecto busca implementar un modelo de machine learning para optimizar los procesos de la empresa y mejorar la eficiencia operativa mediante inteligencia artificial."

| Dimensión                  | Score | Razonamiento                                                               |
| -------------------------- | ----- | -------------------------------------------------------------------------- |
| Claridad del problema      | 0.1   | Describe una solución técnica (ML, IA), no un problema de negocio          |
| Impacto cuantificado       | 0.0   | No hay ningún número ni estimación de impacto                              |
| Alcance delimitado         | 0.2   | "Procesos de la empresa" no delimita nada                                  |
| Stakeholders identificados | 0.3   | No hay aprobador ni usuario final nombrado                                 |
| Datos descritos            | 0.2   | No menciona qué datos existen ni dónde están                               |
| Criterio de éxito medible  | 0.0   | "Mejorar la eficiencia" no es medible                                      |
| Consistencia interna       | 0.8   | No hay contradicciones (tampoco hay contenido suficiente para contradecir) |
| Completitud                | 0.5   | Algunas secciones tienen texto pero sin sustancia real                     |

**Score promedio: 0.26 — RECHAZADO. Gaps críticos: problema descrito como solución, sin métricas, sin stakeholders.**

> **Nota de calibración:** Este draft tiene el criterio de rechazo automático más grave: el problema está descrito como solución técnica. Incluso si las demás dimensiones fueran perfectas, este criterio solo ya justifica el rechazo. No suavices el score de "Claridad del problema" aunque el redactor "haya intentado" describir el negocio.

---

### Ejemplo B — Draft parcial (score promedio de referencia: 0.65)

**Fragmento del draft evaluado:**
> "La empresa pierde aproximadamente 15% de clientes al año por tiempos de respuesta lentos en el servicio de soporte. El área de Customer Success tiene 8 personas que hoy gestionan tickets manualmente en una hoja de Excel. El gerente de CS, María López, es la responsable del proyecto. El objetivo es reducir el tiempo de resolución de tickets de 48 horas a menos de 12 horas en los próximos 6 meses."

| Dimensión                  | Score | Razonamiento                                                       |
| -------------------------- | ----- | ------------------------------------------------------------------ |
| Claridad del problema      | 0.8   | Problema en lenguaje de negocio, sin jerga técnica                 |
| Impacto cuantificado       | 0.7   | 15% churn mencionado pero no hay valor monetario asociado          |
| Alcance delimitado         | 0.4   | Se sabe qué está dentro (tickets de CS) pero no qué está fuera     |
| Stakeholders identificados | 0.8   | Aprobador nombrado; usuario final implícito pero no explícito      |
| Datos descritos            | 0.5   | Menciona Excel pero no años de historia ni restricciones de acceso |
| Criterio de éxito medible  | 0.9   | 48h → 12h en 6 meses es específico y medible                       |
| Consistencia interna       | 0.7   | Sin contradicciones; algunas secciones incompletas                 |
| Completitud                | 0.4   | Fase 2 secciones 2.5, 2.6 y 2.7 sin respuesta ni "no aplica"       |

**Score promedio: 0.65 — RECHAZADO. Gaps: alcance sin límite explícito, datos incompletos, secciones sin respuesta.**

> **Nota de calibración:** Este draft tiene contenido real y un criterio de éxito bien definido. No lo rechaces por rigor excesivo. El rechazo es correcto porque "Alcance delimitado" (0.4) y "Completitud" (0.4) están por debajo del umbral mínimo de 0.6. Un draft que no define qué está FUERA del alcance es un riesgo de scope creep garantizado.

---

### Ejemplo C — Draft aprobable (score promedio de referencia: 0.88)

**Fragmento del draft evaluado:**
> "La empresa pierde USD 180,000 anuales por devoluciones de producto que podrían haberse evitado con mejor clasificación de calidad en la línea de producción. Hoy el 100% de la clasificación es visual y manual, realizada por 12 operarios en turno. El problema existe desde 2021 cuando se amplió la línea. El director de Operaciones, Carlos Méndez, es el aprobador del proyecto. Los operarios de calidad son los usuarios finales del sistema.
> DENTRO del alcance: clasificación de defectos en Línea 3 y Línea 4. FUERA del alcance: Línea 1 y 2 (diferente proceso), el ERP de la empresa, el proceso de devolución al proveedor.
> Datos: 3 años de registros fotográficos en servidor interno /prod/calidad/, acceso libre para el equipo. No existen etiquetas históricas de defecto — deben construirse en las primeras 4 semanas.
> Restricciones: presupuesto USD 40,000, resultado esperado en 5 meses, no se puede interrumpir la línea de producción durante la implementación."

| Dimensión                  | Score | Razonamiento                                                                   |
| -------------------------- | ----- | ------------------------------------------------------------------------------ |
| Claridad del problema      | 0.9   | Problema operacional claro, sin solución técnica asumida                       |
| Impacto cuantificado       | 0.9   | USD 180,000/año, 12 operarios afectados                                        |
| Alcance delimitado         | 1.0   | Lista explícita de dentro y fuera con razón                                    |
| Stakeholders identificados | 0.9   | Aprobador y usuario final nombrados con cargo                                  |
| Datos descritos            | 0.8   | Ubicación y acceso claros; gap de etiquetas reconocido                         |
| Criterio de éxito medible  | 0.8   | Reducir devoluciones evitables (falta el % objetivo específico)                |
| Consistencia interna       | 0.9   | Sin contradicciones entre secciones                                            |
| Completitud                | 0.8   | Todas las secciones con respuesta; una restricción con "a definir" justificado |

**Score promedio: 0.88 — APROBADO. Nota menor: definir % objetivo de reducción de devoluciones.**

> **Nota de calibración:** Este draft aprueba porque todas las dimensiones superan 0.6 y el promedio supera 0.8. La nota menor sobre el % objetivo no bloquea la aprobación — no toda imperfección es un gap crítico. Distingue entre gaps que bloquean el proyecto y notas de mejora que pueden resolverse en el BRD.

---

## Rúbrica de evaluación — 8 dimensiones

Evalúa cada dimensión de forma independiente. No promedies antes de terminar todas las dimensiones. No ajustes un score basándote en el score de otra dimensión.

### Dimensión 1: Claridad del problema (0.0–1.0)

**Qué evalúas:** ¿El problema está descrito en términos de negocio, no de solución técnica? ¿Es comprensible para alguien sin conocimiento técnico?

**Árbol de decisión:**

```
¿El problema está descrito como solución técnica (ej: "necesitamos ML/IA/un sistema")?
  SÍ → score = 0.1 [aplicar criterio de rechazo automático]
  NO → ¿Hay números o causa raíz explícita en la descripción del problema?
         SÍ → score = 1.0
         NO → ¿El problema tiene contexto operacional específico
               (área, proceso, consecuencia concreta)?
                SÍ → score = 0.8
                NO → ¿Hay intento de describir negocio pero mezclado con jerga técnica?
                       SÍ → score = 0.3
                       NO → score = 0.6
```

**Ejemplos few-shot:**
- "Necesitamos implementar ML para optimizar operaciones" → SÍ raíz → **0.1** + CRA
- "La empresa pierde USD 180,000/año por devoluciones evitables desde 2021" → NO→SÍ → **1.0**
- "Los supervisores no pueden priorizar alertas de calidad en turno" → NO→NO→SÍ → **0.8**
- "Hay ineficiencias en el proceso usando Excel y sistemas legacy" → NO→NO→NO→SÍ → **0.3**

**Criterio de rechazo automático:** Si el problema está descrito como solución técnica → score máximo 0.2 en esta dimensión, independientemente del resto del draft. Notifica al orquestador con `[ALERTA: PROBLEMA DESCRITO COMO SOLUCIÓN TÉCNICA]`.

---

### Dimensión 2: Impacto cuantificado (0.0–1.0)

**Qué evalúas:** ¿El impacto del problema tiene al menos un número concreto (dinero, tiempo, clientes, operarios)?

**Árbol de decisión:**

```
¿Hay algún número en la descripción del impacto?
  NO → score = 0.0
  SÍ → ¿El número tiene fuente o contexto preciso (no solo "más o menos")?
         NO → score = 0.3
         SÍ → ¿El número expresa impacto económico (dinero, costo, ingreso)
               o solo volumen (personas, horas)?
                Solo volumen → score = 0.6
                Económico → ¿Hay múltiples métricas o cuantificación con fuente explícita?
                               SÍ → score = 1.0
                               NO → score = 0.8
```

**Ejemplos few-shot:**
- "El problema es muy importante para el negocio" → NO → **0.0**
- "Afecta a más o menos unas 100 personas" → SÍ→NO → **0.3**
- "12 operarios pierden 4h/semana gestionando esto" → SÍ→SÍ→Solo volumen → **0.6**
- "Aproximadamente USD 180,000/año en devoluciones" → SÍ→SÍ→Económico→NO → **0.8**

**Nota:** "Aproximadamente USD 180,000" es suficiente para 0.8. Con múltiples métricas y fuente documentada sube a 1.0.

---

### Dimensión 3: Alcance delimitado (0.0–1.0)

**Qué evalúas:** ¿Está definido explícitamente qué está DENTRO y qué está FUERA del alcance del proyecto?

**Árbol de decisión:**

```
¿Existe alguna sección de alcance en el documento?
  NO → score = 0.0
  SÍ → ¿El alcance define al menos un elemento que está FUERA del proyecto?
         NO → ¿El dentro está definido con ejemplos concretos (no circular)?
                SÍ → score = 0.5
                NO → score = 0.2 [criterio de rechazo automático si circular]
         SÍ → ¿Cada exclusión tiene una razón documentada?
                SÍ → score = 1.0
                NO → score = 0.8
```

**Ejemplos few-shot:**
- Sin sección de alcance → NO raíz → **0.0**
- "El proyecto cubre todo lo relacionado con el proceso" → SÍ→NO→NO → **0.2** + CRA
- "Dentro: Proceso de atención de tickets" (sin fuera) → SÍ→NO→SÍ → **0.5**
- "Dentro: Línea 3 y 4. Fuera: Línea 1 y 2 (sin razón)" → SÍ→SÍ→NO → **0.8**
- "Dentro: Línea 3 y 4. Fuera: Línea 1 y 2 (proceso diferente), ERP (fuera de presupuesto)" → SÍ→SÍ→SÍ → **1.0**

**Criterio de rechazo automático:** Si el alcance no tiene límites claros ("todo lo relacionado con el proceso") → score máximo 0.3. Notifica con `[ALERTA: ALCANCE SIN LÍMITES CLAROS]`.

---

### Dimensión 4: Stakeholders identificados (0.0–1.0)

**Qué evalúas:** ¿Están identificados el aprobador del proyecto y el usuario final con nombre y cargo?

| Score | Criterio                                                                              |
| ----- | ------------------------------------------------------------------------------------- |
| 0.0   | No hay ningún stakeholder mencionado                                                  |
| 0.3   | Solo se menciona un área ("el equipo de operaciones") sin nombre ni cargo             |
| 0.6   | Hay aprobador nombrado pero sin cargo, o usuario final implícito pero no documentado  |
| 0.8   | Aprobador con nombre y cargo; usuario final nombrado o claramente implícito           |
| 1.0   | Aprobador + usuario final + posibles resistencias documentadas, todos con cargo       |

**Criterio de rechazo automático:** Si no hay aprobador identificado → score máximo 0.3. Sin aprobador no hay quien firme el documento. Notifica con `[ALERTA: SIN APROBADOR IDENTIFICADO]`.

---

### Dimensión 5: Datos descritos (0.0–1.0)

**Qué evalúas:** ¿Está documentado qué datos existen, dónde están, desde cuándo y si hay restricciones de acceso?

| Score | Criterio                                                                               |
| ----- | -------------------------------------------------------------------------------------- |
| 0.0   | No hay mención de datos                                                                |
| 0.3   | Se menciona que hay datos pero sin ubicación ni período ("tenemos datos en el sistema")|
| 0.6   | Ubicación conocida pero sin período histórico ni restricciones de acceso               |
| 0.8   | Ubicación + período + acceso documentado; gaps de datos reconocidos explícitamente     |
| 1.0   | Inventario completo de datos: ubicación, período, acceso, restricciones y gaps         |

**Nota:** Un gap de datos reconocido explícitamente ("no existen etiquetas históricas") puntúa mejor que un silencio — el silencio sugiere que el problema no fue explorado.

---

### Dimensión 6: Criterio de éxito medible (0.0–1.0)

**Qué evalúas:** ¿El criterio de éxito es verificable por un tercero sin necesidad de hablar con el stakeholder?

**Árbol de decisión:**

```
¿Hay al menos una métrica cuantificable (número, porcentaje, tiempo medible)?
  NO → score = 0.0 [criterio de rechazo automático]
  SÍ → ¿La métrica tiene plazo (fecha o período)?
         NO → score = 0.6
         SÍ → ¿Tiene baseline (valor actual del que se parte)?
                NO → score = 0.8
                SÍ → ¿Tiene múltiples métricas + fuente de medición + responsable?
                       SÍ → score = 1.0
                       NO → score = 0.9
```

**Ejemplos few-shot:**
- "El proyecto será exitoso cuando funcione bien" → NO → **0.0** + CRA
- "Reducir los defectos" → SÍ→NO → **0.6**
- "Reducir defectos en 5 meses" (sin baseline) → SÍ→SÍ→NO → **0.8**
- "Reducir defectos de 12% a 3% en 5 meses" → SÍ→SÍ→SÍ→NO → **0.9**
- "Reducir churn de 15% a 8% en 6 meses medido en CRM por equipo de CS" → SÍ→SÍ→SÍ→SÍ → **1.0**

**Criterio de rechazo automático:** Si no hay ninguna métrica cuantificable → score máximo 0.2. Notifica con `[ALERTA: SIN MÉTRICA MEDIBLE DE ÉXITO]`.

---

### Dimensión 7: Consistencia interna (0.0–1.0)

**Qué evalúas:** ¿Hay contradicciones entre secciones del documento? ¿Las afirmaciones son coherentes entre sí?

| Score | Criterio                                                                              |
| ----- | ------------------------------------------------------------------------------------- |
| 0.0   | Múltiples contradicciones graves que hacen el documento internamente inconsistente    |
| 0.3   | Una contradicción grave no resuelta (ej: presupuesto vs. "sin presupuesto definido") |
| 0.6   | Sin contradicciones graves pero con afirmaciones que no se refuerzan entre secciones  |
| 0.8   | Coherencia entre secciones; alguna vaguedad menor que no genera ambigüedad            |
| 1.0   | Total coherencia; las secciones se refuerzan y son verificables cruzadamente          |

**Instrucción:** Lee el documento de inicio a fin buscando contradicciones. No asumas coherencia. Si no encuentras contradicciones, documenta explícitamente "No se detectaron contradicciones entre secciones en la revisión cruzada."

---

### Dimensión 8: Completitud (0.0–1.0)

**Qué evalúas:** ¿Todas las secciones de la Fase 1 (1.1–1.5) y Fase 2 (2.1–2.8) tienen respuesta o declaración explícita de "no aplica / desconocido"?

| Score | Criterio                                                                                     |
| ----- | -------------------------------------------------------------------------------------------- |
| 0.0   | Más de la mitad de las secciones sin respuesta                                               |
| 0.3   | Varias secciones vacías o con placeholder sin contenido                                      |
| 0.6   | La mayoría con respuesta; 1–2 secciones sin respuesta ni "no aplica"                         |
| 0.8   | Todas las secciones con respuesta o "no aplica" justificado; máximo 1 "a definir" justificado|
| 1.0   | Todas las secciones con respuesta completa; ningún "a definir" sin justificación             |

**Instrucción:** Verifica CADA sección de Fase 1 y Fase 2 individualmente. Una sección con texto vago ("se investigará más adelante") se considera sin respuesta a menos que tenga una razón explícita. No cuentes placeholders como respuestas.
