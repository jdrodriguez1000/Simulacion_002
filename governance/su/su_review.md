# su_review.md — Evaluación del Borrador SU.md v1

| Campo | Valor |
|-------|-------|
| **Documento evaluado** | governance/su/su_draft_v1.md |
| **Versión evaluada** | v1 |
| **Agente evaluador** | su_evaluator |
| **Fecha de evaluación** | 2026-05-14 |
| **Score final** | 0.95 |
| **Veredicto** | APROBADO |

---

## 1. SCORES POR DIMENSIÓN

| # | Dimensión | Peso | Score | Contribución |
|---|-----------|------|-------|--------------|
| 1 | Completitud de secciones | 15% | 1.0 | 0.150 |
| 2 | Especificidad del problema | 15% | 0.9 | 0.135 |
| 3 | Criterios de éxito medibles | 15% | 1.0 | 0.150 |
| 4 | Riesgos y dependencias | 15% | 0.9 | 0.135 |
| 5 | Stakeholders y estructura de decisión | 10% | 0.9 | 0.090 |
| 6 | Datos y viabilidad técnica | 15% | 1.0 | 0.150 |
| 7 | Alcance y restricciones | 10% | 1.0 | 0.100 |
| 8 | Transferencia y sostenibilidad | 5% | 0.8 | 0.040 |
| | **TOTAL** | **100%** | **0.95** | **0.950** |

---

## 2. ANÁLISIS POR DIMENSIÓN

### D1 — Completitud de secciones | Score: 1.0

Las 9 secciones obligatorias están presentes y desarrolladas con profundidad sustancial. No hay secciones superficiales ni ausentes. El nivel de detalle es consistente a lo largo del documento.

**Fortalezas:** Cada sección es autosuficiente y referencia correctamente a otras cuando hay dependencias entre ellas. El encabezado incluye stakeholders con roles claros. La Sección 8 (Arquitectura) está desarrollada con diagrama de flujo, política de fallos y decisiones técnicas pendientes explícitas.

### D2 — Especificidad del problema | Score: 0.9

El problema de negocio está cuantificado con métricas concretas: fill rate 87%, días de inventario 90, costo de capital inmovilizado COP 12.000M, impacto por punto porcentual de fill rate COP 800M/año. Las consecuencias tienen fechas específicas dentro del año fiscal 2026. El antecedente del módulo ERP fallido está documentado con causas específicas.

**Deducción (−0.1):** Las métricas de fill rate y días de inventario no declaran explícitamente su fuente de origen (¿reportes SAP? ¿medición interna de Supply Chain? ¿auditoría externa?). Tampoco tienen fecha de última medición. Si en documentos posteriores alguien pregunta "¿este 87% es de cuándo y quién lo calculó?", el documento no responde. Para v2, agregar origen y fecha de cada métrica financiera crítica.

### D3 — Criterios de éxito medibles | Score: 1.0

Criterios cuantitativos a 6 meses (diciembre 2026) y a 12 meses (mayo 2027) con umbrales específicos (MAPE < 20%, fill rate ≥ 91%, ≤ 65 días de inventario, ≥ 80% órdenes referenciando modelo). Tabla de zonas grises con lógica de decisión explícita por rango de fill rate. Criterios cualitativos de adopción identificados con nombres propios (Laura Gómez y Roberto Sánchez deben declarar explícitamente). Autoridad de decisión para producción definida (SPONSOR + aval Laura). Tasa de intervención como métrica progresiva de adopción.

**Sin deducción:** Ningún gap relevante encontrado en esta dimensión.

### D4 — Riesgos y dependencias | Score: 0.9

Tabla de dependencias críticas con responsable y plazo para cada ítem. Riesgos de adopción documentados con plan de escalada en tres escalones (semanas 1, 3 y 5). Períodos de indisponibilidad de stakeholders cuantificados. Condiciones de entrada al proyecto declaradas como prerrequisitos formales (no supuestos).

**Deducción (−0.1):** Dos planes de contingencia permanecen como [PENDIENTE] con responsable asignado pero sin fecha de resolución en el SU.md: (1) plan de contingencia ante salida de Roberto Sánchez antes de octubre 2026; (2) validación de capacidad del equipo de BI. Ambos tienen responsable (SPONSOR) y plazo relativo ("antes del kick-off"), pero no tienen fecha calendario. Si el kick-off no tiene fecha fija aún, estos pendientes no tienen cierre verificable.

### D5 — Stakeholders y estructura de decisión | Score: 0.9

Mapa de 9 stakeholders con nombre, cargo, rol en el proyecto y disponibilidad. Flujo de aprobación para cuatro tipos de decisión: órdenes de compra, paso a producción, cambios de alcance, declaración de fracaso. Riesgos de adopción nominados individualmente (Roberto Sánchez, planeadores con >8 años).

**Deducción (−0.1):** Tres stakeholders de alto impacto no tienen nombre registrado: CFO, CEO y Gerente de Compras. El Gerente de Compras, en particular, tiene un rol de aprobación formal (órdenes >COP 50M) y aparece como condición de entrada al kick-off. No conocer su nombre no bloquea el SU.md, pero sí puede generar ambigüedad en documentos de diseño posteriores que necesiten identificar al firmante.

### D6 — Datos y viabilidad técnica | Score: 1.0

Cinco fuentes de datos identificadas con formato, mecanismo de acceso y estado. Calidad de datos documentada con tres causas específicas de degradación (migración SAP, códigos de devolución incorrectos, portafolio nuevo) y cinco períodos problemáticos identificados con su tratamiento propuesto. Historial realmente utilizable declarado explícitamente: 2022–2025. Seis supuestos técnicos críticos listados, dos marcados como condiciones de entrada. Restricciones de acceso (horario nocturno, ventana de mantenimiento SAP julio) documentadas.

**Sin deducción:** El nivel de granularidad en esta sección supera lo habitual para un SU.md y reduce significativamente el riesgo de descubrimientos tardíos durante la construcción.

### D7 — Alcance y restricciones | Score: 1.0

Alcance piloto específico: 300 SKUs tipo A, 3 bodegas (Bogotá, Medellín, Cali = 70% del volumen), con distinción post-auditoría entre modelo principal (210–230 SKUs) y modelo de fallback (70–90 SKUs) etiquetado explícitamente. Lista de 7 exclusiones explícitas para v1. Cinco restricciones no negociables declaradas. Cuatro decisiones técnicas requeridas antes del inicio de construcción con nivel de obligatoriedad indicado.

**Sin deducción:** La distinción entre SKUs con historial limpio y SKUs de fallback es una decisión de diseño bien fundamentada que reduce el riesgo de comprometer métricas de éxito por incluir SKUs problemáticos en el denominador.

### D8 — Transferencia y sostenibilidad | Score: 0.8

Dueño operativo identificado (Laura Gómez, desde enero 2027). Capacidad requerida del equipo de BI descrita con tres competencias específicas. Plan de transferencia activo durante el desarrollo (no solo al cierre). Tres entregables de documentación obligatorios definidos. Criterio de fracaso de transferencia declarado explícitamente.

**Deducción (−0.2):** La validación de capacidad del equipo de BI es un [PENDIENTE] sin fecha calendario concreta. Si el equipo de BI no tiene el stack (Azure Data Factory, Python, Azure ML), el plan de transferencia actual es inviable y requeriría recursos adicionales no presupuestados. Esta brecha no bloquea el SU.md pero debe resolverse antes del kick-off para que el documento de arquitectura asuma capacidades reales.

---

## 3. PRUEBAS DE ESTRÉS APLICADAS

Las siguientes pruebas adversariales fueron aplicadas al draft:

**PE-1 ¿Qué pasa si el CEO no aprueba el presupuesto el 2026-05-21?**
El documento lo anticipa: distingue actividades que pueden iniciarse sin presupuesto comprometido (levantamiento de datos, análisis exploratorio, diseño de arquitectura) de actividades que requieren aprobación. Esto es correcto y reduce el riesgo de parálisis.

**PE-2 ¿Qué pasa si Roberto Sánchez rechaza activamente el sistema durante el piloto?**
El documento tiene un plan de escalada en tres escalones con fechas relativas y decisión final explícita (continuar con Andrés Torres como referente). El plan es ejecutable aunque depende de la voluntad del SPONSOR de tener la conversación difícil en semana 3.

**PE-3 ¿Qué pasa si el acceso a SAP B1 revela que las tablas no tienen la granularidad esperada?**
Correctamente marcado como supuesto crítico 1 (condición de entrada). El documento dice que sin este supuesto validado "no hay proyecto". Esta es la respuesta correcta: no minimizar el riesgo sino declararlo como bloqueante.

**PE-4 ¿Son los criterios de éxito a 6 meses alcanzables dado el historial de datos?**
El documento reconoce que el historial limpio es 2022–2025 (3 años). Un MAPE < 20% en SKUs tipo A con 3 años de historia, estacionalidad identificada y pipeline semanal es un objetivo difícil pero no irrazonable. La zona gris de fill rate (87%–91%) cubre escenarios intermedios con lógica de decisión clara. Ninguna inconsistencia detectada.

**PE-5 ¿El mecanismo de override es técnicamente viable en el plazo comprometido?**
La Power App embebida en Power BI es factible, pero la compatibilidad móvil está marcada como [PENDIENTE] con "requisito no negociable de Laura". Si Carlos valida en semana 1 que Power Apps no es compatible en móvil, se necesita un plan B que no está documentado. Este es el único riesgo técnico sin alternativa explícita.

---

## 4. GAPS PARA RESOLVER EN v2

Los siguientes gaps deben ser resueltos antes de que el SU.md se considere cerrado para documentos de diseño posteriores. Ninguno es criterio de rechazo, pero todos deben tener cierre verificable:

| ID | Gap | Sección | Responsable | Prioridad |
|----|-----|---------|-------------|-----------|
| G1 | Fuente y fecha de las métricas de fill rate y días de inventario | §2 | SPONSOR | MENOR |
| G2 | Estructura del Excel de promociones (consistente o inconsistente) | §5, §8 | Carlos Méndez | MENOR |
| G3 | Validación de capacidad real del equipo de BI (stack Azure + Python) | §9 | SPONSOR + Carlos | MENOR |
| G4 | Plan de contingencia documentado ante salida de Roberto Sánchez antes de oct 2026 | §7 | SPONSOR | MENOR |
| G5 | Mecanismo técnico para marcaje de SKUs especiales (demanda intermitente, pedidos únicos, discontinuados) | §3 | Carlos Méndez | MENOR |
| G6 | Plan B para override móvil si Power Apps resulta incompatible en semana 1 | §8 | Carlos Méndez | MENOR |
| G7 | Nombres del Gerente de Compras y CFO | §4 | SPONSOR | INFORMATIVO |

---

## 5. CRITERIOS DE RECHAZO AUTOMÁTICO

| Criterio | Estado |
|----------|--------|
| score_final < 0.5 | NO APLICA — score = 0.95 |
| Dos o más dimensiones < 0.6 | NO APLICA — mínimo = 0.8 |
| Dimensión 2 (especificidad del problema) < 0.5 | NO APLICA — D2 = 0.9 |
| Dimensión 3 (criterios de éxito) < 0.5 | NO APLICA — D3 = 1.0 |

**criterios_rechazo_automatico: false**

---

## 6. VEREDICTO

```
APROBADO
score_final: 0.95
dimensiones_bajo_0.6: ninguna
gaps_pendientes: 7 (todos MENORES o INFORMATIVOS)
condición: gaps G1–G6 deben resolverse antes del inicio de construcción
```

El borrador su_draft_v1.md es aprobado para avanzar al siguiente documento del harness. La calidad del draft supera el umbral de aprobación automática (0.8) por un margen significativo. Los 7 gaps identificados no comprometen la validez del acuerdo de entendimiento compartido; deben resolverse como condiciones de entrada a la fase de diseño, no como bloqueos al SU.md.

El documento demuestra aprendizaje explícito del episodio del ERP fallido, lo cual reduce materialmente el riesgo de rechazo por adopción — el riesgo técnico más alto del proyecto.

---

## 7. AUDITORÍA INDEPENDIENTE — doc_auditor

**Veredicto del auditor:** El documento NO supera la auditoría en su estado actual.

### Hallazgos del auditor

| ID | Tipo | Descripción | Secciones |
|----|------|-------------|-----------|
| GC-01 | gap_critico | Ambigüedad piloto vs. producción — impide validar si el objetivo de diciembre 2026 es alcanzable con el cronograma propuesto | S6, S7, S4 |
| CT-01 | contradiccion | Duración del piloto: draft dice 6 semanas; transcript (SPONSOR, 2.3.b) dice 5 semanas | S6 |
| CT-02 | contradiccion | Planeadores adicionales: "6" en encabezado pero desglose suma 5; falta 1 planeador de Bebidas | S4 |
| CT-03 | contradiccion | Criterio fracaso Laura: draft captura umbral de 2-3 semanas pero omite el umbral de 1 mes | S6 |
| CRA-01 | cra | Estructura de gobernanza (quién puede declarar producción/fracaso) declarada como definitiva antes de aprobación del CEO (pendiente sem. 2026-05-21) | S4, S6 |
| GM-01 | gap_menor | Lead time de proveedores (12-18 días) ausente — fundamento de las alertas a 15 días y horizonte de 4-6 semanas | S3, S6 |
| GM-02 | gap_menor | Duración de auditoría de datos (3 semanas, recomendación Carlos) ausente del cronograma | S7, S8 |
| GM-03 | gap_menor | Narrativa para separar desempeño del modelo vs. fill rate global (acordada con CEO desde kick-off) no capturada | S6 |

### Gap crítico GC-01 — Detalle

El draft usa "producción" en Sección 7 (el modelo debe estar en producción el 1 de septiembre) y "piloto" en Sección 6 (inicia última semana agosto, 5-6 semanas en paralelo) sin aclarar si son la misma etapa o etapas consecutivas. Si son etapas separadas, "producción" ocurriría en octubre, dejando solo 2 meses antes de diciembre — insuficiente bajo la premisa declarada de 3 meses mínimos. El argumento de viabilidad temporal colapsa.

**Resolución:** Aclarar explícitamente que el inicio del piloto (última semana agosto) = inicio de producción. Los planeadores usan el modelo en producción desde el primer día — no hay "pase a producción" posterior al piloto.

### CRA-01 — Detalle

El draft describe la autoridad del SPONSOR para declarar producción/fracaso como definitiva, cuando la alineación del CEO (con posibilidad de modificar alcance o detener el proyecto) está agendada para la semana del 2026-05-21. Usar este documento antes de esa reunión puede crear expectativas no validadas.

**Resolución:** Agregar al SU.md: "La estructura de autoridad descrita en esta sección está condicionada a la aprobación del CEO (reunión pendiente semana 2026-05-21). En caso de aprobación parcial o ajuste de alcance, esta estructura debe revisarse."

### Resumen auditor

- gaps_criticos: 1
- gaps_menores: 3
- contradicciones: 3
- cra_presentes: 1

---

## 8. RESUMEN PARA EL ORQUESTADOR

```
Score final (su_evaluator): 0.95
Veredicto su_evaluator: APROBADO
Veredicto doc_auditor: NO SUPERA (gap crítico GC-01 + CRA-01)
Dimensiones bajo 0.6: ninguna
Criterio de rechazo automático: NO
Todos los gaps son TÉCNICOS: NO (GC-01 es redaccional, CRA-01 es de gobernanza)
```
