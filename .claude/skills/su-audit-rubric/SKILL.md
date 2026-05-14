---
name: su-audit-rubric
description: Rúbrica de auditoría para el SU.md. Carga 8 dimensiones con síntomas de gap, 4 criterios de rechazo automático (CRA) y 3 ejemplos de calibración. Invocada por doc_auditor al inicio del Paso 2.
user-invocable: false
---

# Skill: /su-audit-rubric

Rúbrica de auditoría para el documento SU.md. Contiene las 8 dimensiones con síntomas de gap, los 4 criterios de rechazo automático (CRA) y los 3 ejemplos de calibración. Invocada por `doc_auditor` al inicio del Paso 2.

---

## Dimensiones del SU.md y síntomas de gap

| Dimensión | Pregunta de auditoría | Síntoma de gap CRITICO | Síntoma de gap MENOR |
|-----------|----------------------|----------------------|---------------------|
| Claridad del problema | ¿El problema está en lenguaje de negocio sin soluciones técnicas? | Menciona tecnologías, arquitecturas o herramientas **como el problema en sí** (no como restricción) | Lenguaje técnico mezclado con lenguaje de negocio pero el problema sigue siendo identificable |
| Impacto cuantificado | ¿Hay al menos una métrica de impacto con un número? | Frases como "pérdidas significativas", "impacto alto", "muchos errores" sin ningún número | Hay un número pero no tiene unidad, período o contexto claro (ej: "pierde el 15%" sin referencia de base) |
| Alcance delimitado | ¿Hay lista explícita de lo que está DENTRO **y** FUERA? | Solo hay lista de lo que está dentro; la sección FUERA está vacía, ausente o dice "a definir" | Lista de FUERA existe pero es incompleta o ambigua |
| Stakeholders identificados | ¿Hay un aprobador nombrado y un usuario final identificado? | No hay nombre de aprobador; o dice "el gerente" sin nombre ni cargo específico | Aprobador nombrado pero usuario final solo implícito o con área sin cargo |
| Datos disponibles | ¿Se sabe qué datos existen, dónde están y si son accesibles? | "Tenemos datos" sin ubicación, o "datos en el sistema" sin especificar cuál | Ubicación conocida pero sin información de acceso o sin cantidad aproximada |
| Criterio de éxito medible | ¿Hay al menos una métrica de negocio cuantificable con valor objetivo? | "Mejorar la eficiencia", "reducir errores", "optimizar el proceso" sin número objetivo | Hay métrica pero sin valor objetivo o sin plazo definido |
| Consistencia interna | ¿No hay contradicciones entre secciones? | El alcance excluye algo que los criterios de éxito asumen como incluido | Una sección usa supuestos distintos a otra pero la contradicción es menor |
| Completitud | ¿Todas las secciones tienen respuesta o "no aplica" justificado? | Sección vacía o con solo "[PENDIENTE]" sin justificación | Sección con respuesta parcial que cubre lo mínimo pero deja preguntas abiertas |

---

## Criterios de rechazo automático (CRA)

Los CRA invalidan el sprint independientemente del score. Su presencia es un defecto fundamental que el synthesizer no puede resolver solo.

| CRA | Criterio | Evidencia que lo confirma |
|-----|---------|--------------------------|
| CRA-1 | El problema está descrito en términos de solución técnica, no de negocio | La sección "Problema central" menciona la tecnología como el problema (no como restricción o contexto) |
| CRA-2 | No hay stakeholder identificado que pueda aprobar | La sección "Stakeholders" no tiene nombre completo del aprobador |
| CRA-3 | El alcance no tiene límites claros ("todo está dentro" o sección FUERA vacía) | La sección de alcance no lista nada explícitamente excluido |
| CRA-4 | No existe ninguna métrica cuantificable de éxito | La sección "Criterios de éxito" no tiene ningún número, porcentaje o valor objetivo |

---

## Ejemplos de calibración

### Ejemplo A — Draft deficiente (calibración: 3 CRA, 5 gaps CRITICOS)

**Fragmento del draft:**
> "El proyecto busca implementar un modelo de machine learning para optimizar los procesos de la empresa y mejorar la eficiencia operativa mediante inteligencia artificial."

**Auditoría esperada:**

| Sección del draft | Tipo | Severidad | Descripción del gap | Corrección recomendada |
|------------------|------|-----------|--------------------|-----------------------|
| Problema central | Vago/Técnico | CRITICO | Describe solución técnica (ML, IA) como el objetivo; no hay problema de negocio identificable | Reescribir en términos de qué está fallando en el negocio y qué impacto tiene |
| Impacto cuantificado | Vago | CRITICO | "Mejorar la eficiencia operativa" sin ningún número, porcentaje ni referencia de base | Agregar métrica concreta: cuánto cuesta el problema actual |
| Stakeholders | Ausente | CRITICO | Sin aprobador nombrado ni usuario final identificado | Nombrar aprobador con nombre completo y cargo |
| Criterio de éxito | Vago | CRITICO | "Mejorar la eficiencia" no es medible; no hay número objetivo | Definir métrica específica con valor objetivo y plazo |
| Alcance | Circular | MENOR | "Procesos de la empresa" no delimita nada; es tautológico | Listar qué procesos específicos están dentro y cuáles están explícitamente fuera |

CRA: CRA-1 (problema técnico), CRA-2 (sin stakeholder), CRA-4 (sin métrica). Total: 3 de 4.

**Nota de calibración:** No suavices la severidad del gap de "Problema central" aunque el redactor "haya intentado" describir el negocio. El criterio es si el texto resultante está en lenguaje de negocio o de solución técnica.

---

### Ejemplo B — Draft parcial (calibración: 1 CRA, 4 gaps, 0 contradicciones)

**Fragmento del draft:**
> "La empresa pierde aproximadamente 15% de clientes al año por tiempos de respuesta lentos en el servicio de soporte. El área de Customer Success tiene 8 personas que hoy gestionan tickets manualmente en una hoja de Excel. El gerente de CS, María López, es la responsable del proyecto. El objetivo es reducir el tiempo de resolución de tickets de 48 horas a menos de 12 horas en los próximos 6 meses."

**Auditoría esperada:**

| Sección del draft | Tipo | Severidad | Descripción del gap | Corrección recomendada |
|------------------|------|-----------|--------------------|-----------------------|
| Alcance FUERA | Ausente | CRITICO | Solo hay lista de lo que está dentro; la sección FUERA está vacía o ausente | Listar explícitamente qué partes del negocio NO deben tocarse |
| Datos disponibles | Incompleto | CRITICO | "Tickets en Excel" mencionado pero sin años de historia, restricciones de acceso ni ubicación del archivo | Agregar: antigüedad de los datos, ubicación exacta, quién tiene acceso |
| Secciones 2.5, 2.6, 2.7 | Ausente | CRITICO | Tres secciones de la entrevista sin respuesta ni "no aplica" justificado | Completar cada sección o marcar "no aplica" con razón |
| Impacto cuantificado | Incompleto | MENOR | 15% de churn mencionado pero sin valor monetario asociado | Agregar estimación de valor monetario del 15% de churn |

CRA: CRA-3 (alcance sin límites claros — no hay lista de FUERA). Total: 1 de 4.

**Nota de calibración:** No actives CRA-2 (sin stakeholder aprobador) si hay nombre y cargo, incluso si el título es "gerente de CS" y no "Director". El criterio es si hay alguien con nombre que pueda aprobar, no el rango jerárquico.

---

### Ejemplo C — Draft aprobable (calibración: 0 CRA, 1 gap MENOR, 0 contradicciones)

**Fragmento del draft:**
> "La empresa pierde USD 180,000 anuales por devoluciones de producto que podrían haberse evitado con mejor clasificación de calidad en la línea de producción. Hoy el 100% de la clasificación es visual y manual, realizada por 12 operarios en turno. El director de Operaciones, Carlos Méndez, es el aprobador del proyecto. Los operarios de calidad son los usuarios finales del sistema.
> DENTRO del alcance: clasificación de defectos en Línea 3 y Línea 4. FUERA del alcance: Línea 1 y 2 (diferente proceso), el ERP de la empresa, el proceso de devolución al proveedor.
> Datos: 3 años de registros fotográficos en servidor interno /prod/calidad/, acceso libre para el equipo. No existen etiquetas históricas de defecto — deben construirse en las primeras 4 semanas.
> Restricciones: presupuesto USD 40,000, resultado esperado en 5 meses, no se puede interrumpir la línea de producción durante la implementación."

**Auditoría esperada:**

| Sección del draft | Tipo | Severidad | Descripción del gap | Corrección recomendada |
|------------------|------|-----------|--------------------|-----------------------|
| Criterio de éxito | Incompleto | MENOR | No especifica el % objetivo de reducción de devoluciones; solo hay implicación de mejora | Agregar: "reducir devoluciones evitables en X% en los primeros N meses" |

CRA: Ninguno. Total: 0 de 4.

**Nota de calibración:** No actives gaps donde el texto es genuinamente claro. La ausencia de gap en "Alcance delimitado" es correcta cuando hay lista explícita DENTRO y FUERA con razón. No inventes problemas donde no los hay.
