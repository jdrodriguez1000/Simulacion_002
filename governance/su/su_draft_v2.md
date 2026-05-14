# SU.md — Shared Understanding
## Sistema de Forecasting de Demanda para Supply Chain

---

## CAMBIOS RESPECTO A VERSIÓN ANTERIOR (v1 → v2)

| ID hallazgo | Tipo | Corrección aplicada | Sección afectada |
|-------------|------|---------------------|-----------------|
| GC-01 / CT-03 | gap_critico + ambigüedad | Agregada oración aclaratoria: el inicio del piloto (última semana agosto) ES el inicio de producción — no hay etapa posterior de "pase a producción" | §6, §7 |
| CRA-01 | cra | Agregada cláusula condicional explícita sobre aprobación del CEO (reunión semana 2026-05-21) en la descripción de la estructura de gobernanza | §4 |
| CT-01 (RESUELTO) | contradicción | Duración del piloto: SPONSOR confirmó que la cifra correcta es **6 semanas** (el transcript fue impreciso en 2.3.b; el draft v1 tenía razón). Las fechas ajustadas: inicio última semana de agosto, cierre segunda semana de octubre — posterior al cierre del presupuesto Q4, lo cual es aceptable dado que el piloto ya está en producción desde el inicio | §6 |
| CT-02 | contradicción | Tabla de planeadores corregida: "6 adicionales" con desglose corregido — Bebidas (2), Alimentos (2), Hogar (2), Personal (1) = 7; revisado según instrucción del SPONSOR: "6 adicionales" excluye a Andrés Torres (ya listado individualmente) + 1 planeador adicional de Bebidas = desglose confirmado en 7 total (Andrés + 6) | §4 |
| CT-03 | contradicción | Criterio de fracaso de Laura: doble umbral capturado — 2-3 semanas para señal de valor inicial, 1 mes como límite definitivo antes de abandonar | §6 |
| GM-01 | gap_menor | Lead time de proveedores (12-18 días) documentado como fundamento de las alertas a 15 días y del horizonte de forecast | §3, §5 |
| GM-02 | gap_menor | Auditoría de datos: 3 semanas de Carlos incluidas explícitamente en la tabla de dependencias | §7 |
| GM-03 | gap_menor | Narrativa separación desempeño del modelo vs. fill rate global agregada en criterios de éxito | §6 |

---

## 1. ENCABEZADO DEL DOCUMENTO

| Campo | Valor |
|-------|-------|
| **Nombre del proyecto** | Sistema de Forecasting de Demanda para Supply Chain |
| **Fecha de creación** | 2026-05-14 |
| **Versión** | v2 — correcciones menores post-revisión de auditor y stakeholder |
| **Versión anterior** | v1 (score evaluador: 0.95, APROBADO; aprobación stakeholder condicionada a correcciones) |
| **Agente sintetizador** | su_synthesizer |

### Stakeholders que participaron en la entrevista

| Nombre | Cargo | Rol en el proyecto | Disponibilidad |
|--------|-------|-------------------|----------------|
| Juan Diego Rodriguez | Director de Data & Analytics | SPONSOR / patrocinador ejecutivo | Punto de contacto principal |
| Carlos Méndez | Data Scientist Senior | TECNICO / responsable del desarrollo | Tiempo completo durante el proyecto |
| Laura Gómez | Jefe de Cadena de Suministro | USUARIO / coordinadora de planeación y usuaria final | Martes y jueves, 1 hora por sesión |

---

## 2. CONTEXTO Y PROBLEMA DE NEGOCIO

### Descripción de la organización

Empresa distribuidora de productos de consumo masivo en Colombia con presencia nacional en 12 ciudades. El área de Supply Chain cuenta con aproximadamente 40 personas: planeadores por categoría, analistas de inventario y coordinadores de compras. La unidad de Data & Analytics (D&A) actúa como área habilitadora del proyecto.

### El problema central

Los planeadores deciden cuándo y cuánto pedir a los proveedores con base en su experiencia personal y en reportes estáticos de Excel. No existe un sistema que anticipe la demanda futura por SKU de forma sistemática. Esto produce dos disfunciones simultáneas y opuestas:

- **Quiebres de stock** en productos de alta rotación, que frenan ventas y deterioran relaciones con clientes clave.
- **Sobrestock** en productos de baja rotación, que inmoviliza capital de trabajo.

El flujo de trabajo actual del lunes ilustra el problema: el equipo de planeación dedica entre 2 y 3 horas solo a diagnosticar el estado del inventario (extracción SAP, construcción del Excel maestro, revisión por categorías) antes de poder tomar decisiones. Ese tiempo de diagnóstico elimina la ventana proactiva de la semana.

### Antecedentes

El problema existe desde hace al menos 3 años. Se intentó resolver con una consultoría externa que implementó un módulo de planeación en el ERP (SAP B1). El módulo fracasó por dos razones documentadas: (1) los pronósticos eran a nivel de categoría, no de SKU, y no reflejaban la estacionalidad real del negocio; (2) los planeadores no fueron involucrados en el diseño — se les presentó la solución terminada y se les pidió que confiaran. El resultado fue rechazo activo. Desde entonces el equipo volvió al Excel propio. Esta lección es determinante para el diseño de adopción del proyecto actual.

### Impacto cuantificado del problema

| Métrica | Estado actual | Objetivo | Impacto monetario |
|---------|--------------|----------|-------------------|
| Fill rate al cliente | 87% | 95% | COP 800M por punto porcentual perdido al año |
| Días de inventario (categorías críticas) | 90 días | 45 días | COP 12.000M capital inmovilizado en exceso |
| Tiempo planeadores en reactivo | ~60% de su tiempo | Reducir a <30% | No cuantificado explícitamente |

### Áreas afectadas y consecuencias críticas

- **Planeación:** 60% del tiempo en modo reactivo (apagar incendios) en lugar de planear a futuro.
- **Comercial:** pérdida de ventas por quiebres y deterioro de relaciones con clientes de canal moderno.
- **Finanzas:** inmovilización de capital de trabajo; objetivo de reducción exigido por la junta para el cierre fiscal 2026.
- **Dirección General:** fill rate es uno de los tres objetivos estratégicos del año.

**Consecuencias con fecha:** riesgo de perder dos contratos con clientes de canal moderno que tienen cláusula de fill rate mínimo del 93%; y riesgo de no cumplir la meta de reducción de capital de trabajo para el cierre fiscal de 2026. Ambas consecuencias tienen fecha concreta dentro del año en curso.

---

## 3. SOLUCIÓN ESPERADA

### Descripción de la solución

Un sistema de forecasting de demanda que entrega, cada lunes antes de las 7am, una vista por SKU y por bodega con tres elementos: (1) pronóstico de demanda para las próximas 4 y 8 semanas, (2) alerta de SKUs en riesgo de quiebre en los próximos 15 días si no se genera una orden, y (3) sugerencia de cantidad y fecha de orden considerando el lead time del proveedor.

El parámetro de lead time de proveedores es de **12 a 18 días** (promedio del portafolio, según Laura Gómez). Este dato es el fundamento técnico de tres decisiones de diseño: (a) las alertas de quiebre se calculan a 15 días — umbral dentro del rango de lead time medio; (b) el horizonte de forecast operativo relevante es de 4 a 6 semanas — el mínimo para que la sugerencia de orden sea accionable antes del quiebre; (c) el forecast a 4 semanas es el horizonte de validación del MAPE. Si el lead time cambia significativamente en segmentos del portafolio, el modelo debe recalibrar el umbral de alerta por grupo de proveedores.

El sistema actúa como **copiloto, no como autopiloto**: la recomendación es un punto de partida; la decisión final siempre la toma el planeador. Las órdenes de compra no se generan automáticamente en SAP — el planeador las visualiza en el dashboard y las ingresa manualmente. Esta restricción es no negociable en v1 y responde directamente a la lección del ERP.

### Funcionalidades principales del sistema

1. Dashboard Power BI semanal (disponible lunes 7am) con forecast por SKU-bodega a 4 y 8 semanas.
2. Alertas automáticas de SKUs en riesgo de quiebre a 15 días, priorizadas por urgencia. Umbral basado en lead time promedio de proveedores (12-18 días).
3. Sugerencia de orden (cantidad + fecha) calculando lead time de proveedor. El modelo usa el parámetro de 12-18 días como referencia; Carlos puede parametrizar por segmento de proveedor si la varianza del lead time lo justifica.
4. Explicación de los tres principales drivers del forecast por SKU por semana, en lenguaje operativo (no estadístico). Ejemplo: "la demanda proyectada es alta principalmente por proximidad a temporada de Navidad y por incremento en ventas de las últimas 3 semanas".
5. Mecanismo de override: el planeador puede registrar un ajuste al forecast del modelo con motivo en texto libre; ambos valores (forecast modelo y forecast ajustado) quedan visibles en paralelo y el ajustado alimenta la recomendación de orden.
6. [PENDIENTE: definir el mecanismo técnico para marcaje de SKUs especiales — demanda intermitente, pedidos por cliente único, SKUs en discontinuación — que deben excluirse del modelo general desde el inicio del piloto; responsable: Carlos Méndez, antes del inicio del piloto.]
7. Vista agregada separada para CFO y Gerente de Compras: capital de trabajo proyectado y fill rate esperado por categoría, con permisos independientes en el mismo workspace de Power BI.

### Reducción de tiempo/esfuerzo esperada

El tiempo de decisión de reorden pasa de **medio día por planeador por categoría** a **30 minutos para toda la cartera**. Para Laura, el lunes cambia de un día de diagnóstico a un día de decisiones: en lugar de recorrer 300 SKUs para encontrar los 20 en riesgo, el sistema prioriza los 20 directamente.

### Criterios de éxito

**A 6 meses (diciembre 2026):**
- Fill rate sube de 87% a mínimo 91%.
- Días de inventario en categorías críticas bajan de 90 a 65 días.
- Al menos 80% de las órdenes de compra generadas en diciembre referencian el forecast del modelo.
- MAPE del forecast a 4 semanas inferior al 20% en SKUs tipo A.

**A 12 meses (mayo 2027):**
- Fill rate en 95% sostenido durante dos meses consecutivos.
- Días de inventario en 45 días.
- Los dos contratos de canal moderno renovados sin penalización por fill rate.

### Restricciones no negociables (v1)

1. Integración con SAP B1 para lectura de inventario y movimientos — sin extracciones manuales.
2. Interpretabilidad: el modelo debe mostrar por qué recomienda lo que recomienda, con los tres drivers principales por predicción individual.
3. Infraestructura en la nube (Azure) con mínima intervención del equipo de IT.
4. Sin adquisición de licencias de software adicionales de costo significativo.
5. Sin generación automática de órdenes de compra en SAP en v1.

---

## 4. STAKEHOLDERS Y ESTRUCTURA DE DECISIÓN

### Mapa completo de stakeholders

| Nombre | Cargo | Rol en el proyecto | Disponibilidad |
|--------|-------|-------------------|----------------|
| Juan Diego Rodriguez | Director D&A | SPONSOR, patrocinador ejecutivo, decisor de alcance y presupuesto | Principal |
| Carlos Méndez | Data Scientist Senior | TECNICO, construcción y entrega del sistema | Tiempo completo |
| Laura Gómez | Jefe de Cadena de Suministro | USUARIO, coordinadora, aval de producción | Mar/Jue, 1h/sesión |
| Roberto Sánchez | Planeador Senior | Usuario clave, influenciador del equipo | Tiempo normal de trabajo |
| Andrés Torres | Planeador de Bebidas | Campeón interno de adopción (perfil analítico, proactivo) | Tiempo normal de trabajo |
| Gerente de Compras | (no nombrado) | Aprueba órdenes >COP 50M; view agregado de outputs | Por demanda |
| CFO | (no nombrado) | Visibilidad de capital de trabajo proyectado | Por demanda |
| CEO | (no nombrado) | Patrocinio estratégico; aprobación del presupuesto | Solo en hitos clave |
| 6 planeadores adicionales | Bebidas (1 adicional al ya listado), Alimentos (2), Hogar (2), Personal (1) | Usuarios finales del dashboard | Tiempo normal |

**Nota sobre conteo de planeadores:** Andrés Torres (Planeador de Bebidas) está listado individualmente como campeón de adopción. Los "6 planeadores adicionales" son: 1 planeador adicional de Bebidas + Alimentos (2) + Hogar (2) + Personal (1) = 6. Total del equipo de planeación en el piloto: Andrés Torres + 6 adicionales = 7 planeadores.

### Flujo de aprobación

- **Órdenes de compra:** planeador → Laura (hasta COP 50M) → Gerente de Compras (>COP 50M).
- **Pasar a producción:** SPONSOR con aval explícito de Laura. Gerente de Compras debe ser informado pero no tiene veto. CEO no necesita aprobar ese paso.
- **Cambios de alcance o presupuesto:** requieren escalar al CEO.
- **Declaración de fracaso:** SPONSOR con input de Laura; CEO entra solo si hay implicación presupuestaria de continuar o detener.

> **[CRA-01 — CLÁUSULA CONDICIONAL]** La estructura de autoridad descrita en esta sección está condicionada a la aprobación del CEO (reunión pendiente semana del 2026-05-21). En caso de aprobación parcial, ajuste de alcance o detención del proyecto, esta estructura de gobernanza debe revisarse antes de usarse como referencia en documentos de diseño posteriores. Los documentos subsiguientes del harness (BRD, SAD) no deben asumir esta estructura como definitiva hasta que el resultado de la reunión CEO sea conocido y registrado.

### Riesgos de adopción identificados

- **Roberto Sánchez (riesgo alto):** 8 años de antigüedad, mayor influencia sobre el equipo. Postura actual: escéptico. Si no adopta, los demás no adoptan. Su condición para el apoyo: poder intervenir el forecast manualmente y que esa intervención quede registrada para aprender de ella.
- **Dos planeadores adicionales con >8 años:** argumentan que "el negocio tiene muchas variables que un modelo no puede capturar". Se abordan por proximidad con Roberto.
- **Lección del ERP:** el rechazo histórico fue causado por no involucrar a los usuarios en el diseño. Estrategia actual: co-diseño del mecanismo de override con Laura y Roberto antes del kick-off, luego presentación general al equipo.
- **Plan de escalada ante resistencia activa:** (1) semanas 1-2: Laura muestra a Roberto datos de intervenciones vs. modelo; (2) semana 3: SPONSOR tiene conversación uno a uno con Roberto; (3) semana 5: si Roberto bloquea activamente al equipo, decisión ejecutiva — piloto continúa con Andrés Torres como referente principal y situación de Roberto se gestiona con RRHH.

### Compromisos pendientes

- **Decisión pendiente: alineación del CEO.** Reunión agendada para la semana del 2026-05-21. Resultado puede ser: aprobación completa del presupuesto, aprobación con ajuste de alcance, o detención del proyecto. Es prerrequisito para comprometer presupuesto, no para iniciar actividades sin inversión (levantamiento de datos, análisis exploratorio, diseño de arquitectura).

---

## 5. DATOS Y SISTEMAS

### Fuentes de datos disponibles

| Fuente | Contenido | Formato / Acceso |
|--------|-----------|-----------------|
| SAP B1 — servidor de reporting | Historial ventas (ORDR/RDR1), inventario (OINM), maestro productos (OITM), órdenes de compra (OPOR/POR1) | SQL Server; solo lectura; credenciales IT (5-10 días hábiles) |
| Excel de planeadores | Seguimiento semanal por SKU de alta rotación (considerado más confiable que SAP por los planeadores) | Archivos propios por planeador; deben centralizarse antes de la auditoría |
| Excel de promociones comerciales | Promociones de canal moderno contratadas | [PENDIENTE: verificar estructura del archivo antes del inicio — si columnas son inconsistentes entre analistas o cambian frecuentemente, se pospone a v2 y en v1 se modelan solo las temporadas conocidas como variables calendario. NOTA: el SPONSOR declaró en entrevista que las promociones "entran en v1" dada su importancia para SKUs tipo A. La condición técnica de Carlos (estructura consistente requerida) puede invalidar este compromiso si el Excel tiene estructura inconsistente. Punto de alineación pendiente SPONSOR-TECNICO antes del kick-off.] |
| Variables calendario codificadas | 4 temporadas altas: Navidad, Semana Santa, regreso a clases, Día de la Madre | Fechas estables; Carlos las construye directamente |
| Precios de lista | En SAP B1 | Incluidos en v1 |
| Lead time de proveedores | Parámetro operativo: 12 a 18 días promedio del portafolio (fuente: Laura Gómez, Fase 2.U del proceso de entrevista) | Dato proporcionado por el área de Supply Chain; debe validarse contra datos históricos de SAP (órdenes de compra OPOR) antes del inicio de construcción |

### Calidad de los datos

El historial confiable real por SKU tipo A es de **28 a 32 meses en promedio** — no 6 años nominales. Tres causas acumuladas:

1. **Migración SAP 2020-2021:** 4 meses con registros incompletos para la mayoría de SKUs; para productos relanzados en ese período el historial pre/post-migración no es comparable.
2. **Códigos de devolución incorrectos:** afectan especialmente SKUs tipo A (alta rotación). Estimación conservadora de Carlos: entre 8% y 15% de salidas registradas en SAP tienen ruido por este problema.
3. **Portafolio nuevo:** ~60 de los 300 SKUs tipo A fueron introducidos después de 2022 y tienen menos de 3 años de historia. Requieren estrategias de cold start.

**Cinco períodos problemáticos identificados:**
- Marzo–junio 2020: pandemia (comportamiento atípico extremo — se modela con variable indicadora de anomalía).
- Octubre 2020–febrero 2021: migración SAP (exclusión definitiva para SKUs con >40% de semanas del período ausentes).
- Diciembre 2021–enero 2022: paro de transportadores nacional (se modela con variable indicadora).
- Períodos de inventario cero por quiebre de stock (dispersos en toda la serie): reconstrucción activa de demanda latente con órdenes pendientes/rechazadas de SAP.
- 2019: menor granularidad; decisión diferida a la auditoría.

**Historial realmente utilizable sin tratamiento especial: 2022-2025.**

### Volumen y granularidad

- ~1.800 SKUs activos totales; clasificación ABC en SAP (300 tipo A = ~80% de ventas).
- Rotación de portafolio: 80-120 SKUs entran/salen por año, principalmente en cuidado personal.
- Piloto v1: 300 SKUs tipo A en 3 bodegas. Post-auditoría: 210-230 SKUs con historial limpio y suficiente (70-77% de los 300); los restantes 70-90 SKUs reciben modelo de fallback (promedio móvil ajustado por estacionalidad) etiquetado explícitamente en el dashboard como "forecast de baja confianza".
- Granularidad de trabajo: demanda diaria por SKU-bodega, construida desde tablas transaccionales SAP.

### Restricciones de acceso y conectividad

- Acceso al servidor de reporting de SAP: **solo lectura**, vía el servidor de reporting (nunca el servidor productivo). Queries SQL directas al backend de SAP B1.
- Proceso de credenciales: Carlos envía solicitud a IT con visto bueno del SPONSOR; IT procesa en 5-10 días hábiles. **Debe iniciarse el día 1 del proyecto.**
- Queries solo en horario nocturno: IT pidió que no corran entre 7am y 6pm. Compatible con el schedule dominical.
- Ventana de mantenimiento SAP: primera semana de julio (actualización del servidor de reporting, 2 días de downtime estimado). No es bloqueo crítico pero debe evitarse extracción masiva esa semana.

---

## 6. CRITERIOS DE ACEPTACIÓN

### Período de prueba y metodología de validación

**El inicio del piloto equivale al inicio de la operación en producción.** Desde la última semana de agosto de 2026, los planeadores utilizan el sistema en producción real — no en un entorno de prueba paralelo separado. El período de operación en paralelo (planeadores mantienen su proceso actual y simultáneamente usan las recomendaciones del modelo, registrando cuándo coinciden y cuándo difieren) es el mecanismo de validación, no una etapa previa a la producción. No existe un "pase a producción" formal posterior al piloto: el sistema está en producción desde el primer día del piloto.

**Duración del piloto:** seis semanas. Inicio: última semana de agosto de 2026. Cierre: segunda semana de octubre de 2026 (el cierre del piloto ocurre después del cierre del presupuesto de compras Q4 de la primera semana de octubre, lo cual es aceptable dado que el sistema ya está en producción desde agosto y los datos del modelo ya informan el proceso de planeación para Q4).

**Aclaración sobre el objetivo de 3 meses:** la premisa de "mínimo 3 meses de uso del modelo para impactar el inventario de diciembre" se cumple contando desde el inicio del piloto (última semana agosto) hasta diciembre 2026 — son aproximadamente 14 semanas (más de 3 meses). El cumplimiento de esta premisa depende de que el piloto inicie en la fecha comprometida.

### Criterios cuantitativos de adopción

- **MAPE < 20%** en el forecast a 4 semanas para SKUs tipo A.
- **≥ 80% de las órdenes de compra** de diciembre 2026 referencian el forecast del modelo.
- Fill rate alcanza ≥ 91% en diciembre 2026.
- Días de inventario en categorías críticas ≤ 65 días en diciembre 2026.

### Separación entre desempeño del modelo y fill rate global

**Advertencia de interpretación (acordada con el SPONSOR para comunicar al CEO desde el kick-off):** el fill rate de diciembre 2026 es un indicador de resultado del negocio, no un indicador directo de la calidad del modelo de forecasting. Factores externos — quiebres en proveedores, variaciones de demanda extraordinarias, decisiones de compra de Gerencia — pueden mover el fill rate independientemente de si el modelo forecast correctamente. Para evaluar el desempeño del modelo de forma aislada, el indicador primario es el **MAPE < 20%** (precisión de la predicción) y la **tasa de adopción** (≥ 80% de órdenes referenciando el modelo). El fill rate es el indicador de impacto de negocio, que requiere meses adicionales de uso consistente para reflejar la calidad del modelo. Esta separación debe comunicarse explícitamente al CEO en el kick-off para evitar que un fill rate por debajo del objetivo en diciembre 2026 se interprete erróneamente como fracaso del modelo.

### Criterios cualitativos de adopción

- Laura Gómez y Roberto Sánchez declaran explícitamente que confían en usar el sistema como punto de partida. **Ambos son obligatorios** — si el número de MAPE es bueno pero Roberto no confía, no hay adopción real.
- Los planeadores usan el sistema de forma genuina, no forzada (distinción entre adopción real y cumplimiento formal).

**Cláusula alternativa ante salida de Roberto Sánchez:** si Roberto Sánchez sale del equipo de planeación antes del cierre del piloto (riesgo documentado en §7), el criterio cualitativo se redefinirá como: "Andrés Torres y al menos 2 planeadores adicionales declaran explícitamente que confían en el sistema". El SPONSOR es responsable de documentar esta redefinición antes del kick-off mediante el plan de contingencia referenciado en §7.

### Tasa de intervención como métrica de adopción progresiva

- Primeras 6 semanas: 40% o más de las recomendaciones intervenidas — normal y esperado.
- A los 6 meses: si la tasa de intervención en SKUs tipo A sigue por encima del 30%, es señal de que el modelo no está aprendiendo o hay variables no capturadas. Dispara revisión de causas.

### Criterios de abandono por parte de la usuaria final (Laura Gómez)

Laura abandonaría el sistema si ocurre alguna de estas cuatro situaciones:
1. El modelo falla en SKUs tipo A sin explicar por qué cambió la predicción (fallos silenciosos son peores que el Excel).
2. **Umbral de paciencia:** después de 2-3 semanas del piloto, el equipo no percibe ninguna señal de valor inicial. Si tras un mes completo de operación los planeadores sienten que hacen más trabajo que con el Excel sin mejora perceptible, Laura declara fracaso y el equipo vuelve al Excel. La diferencia entre ambos umbrales: las primeras 2-3 semanas son el período de observación — Laura espera señales de valor, no resultados definitivos; el mes es el límite definitivo.
3. El dashboard requiere conocimientos estadísticos para interpretarse (lenguaje operativo obligatorio, no percentiles ni intervalos de confianza crudos).
4. El sistema no respeta las excepciones del negocio desde el inicio — trata productos con demanda intermitente, pedidos especiales o en discontinuación como si fueran productos normales.

---

## 7. RESTRICCIONES Y DEPENDENCIAS

### Fecha límite inamovible y justificación

**Última semana de agosto de 2026** — el modelo debe estar en producción (equivalente al inicio del piloto) en esa fecha. Justificación: los planeadores necesitan mínimo 3 meses de uso para que las órdenes influenciadas por el modelo impacten el inventario disponible en diciembre 2026. Adicionalmente, para que la prueba de 6 semanas capture datos de Q4 antes del cierre del presupuesto de compras en la primera semana de octubre, el inicio en la última semana de agosto es la fecha mínima viable.

### Dependencias críticas

| Dependencia | Responsable | Plazo |
|-------------|-------------|-------|
| Credenciales de acceso al servidor de reporting SAP | Carlos solicita, IT procesa, SPONSOR avala | Día 1 del proyecto (5-10 días hábiles de trámite) |
| Aprobación del CEO para presupuesto | SPONSOR | Semana del 2026-05-21 |
| Declaración de fuente de verdad (SAP vs. Excel) | SPONSOR + Laura + Gerente de Compras | Kick-off (condición de entrada, no supuesto) |
| Documento de eventos históricos de Laura | Laura (2 horas estimadas) | Antes del día 1 de auditoría de datos |
| Acceso a Excel de planeadores (últimos 24 meses) | Laura centraliza | Antes del inicio de auditoría |
| **Auditoría de datos de Carlos** | **Carlos Méndez** | **3 semanas — debe iniciarse en semana 1 del proyecto; es condición de entrada a la fase de construcción del modelo** |
| Conversación con líder de equipo BI sobre capacidad | SPONSOR + Carlos | Antes del kick-off |

**Nota sobre la auditoría de datos:** Carlos estima 3 semanas de trabajo para auditar el historial de SAP (limpieza de períodos problemáticos, evaluación de SKUs con historia insuficiente, decisión sobre los 70-90 SKUs de fallback). Esta auditoría es la actividad de mayor duración en la fase de preparación y debe iniciarse el primer día del proyecto. El resultado de la auditoría determina qué SKUs entran al modelo principal vs. al modelo de fallback.

### Disponibilidad de stakeholders y períodos de riesgo

- **Agosto 2026:** auditoría interna de Supply Chain — Laura disponible solo al 40% durante 2-3 semanas. No puede participar activamente en la prueba al mismo tiempo.
- **Septiembre 2026:** feria sectorial de logística — Laura y Gerente de Compras ausentes 3 días. No bloqueante para la prueba.
- **Riesgo de continuidad — Roberto Sánchez:** tiene conversaciones internas sobre una posible promoción a coordinador regional que lo sacaría del equipo de planeación antes de octubre 2026. Probabilidad estimada baja, pero no nula. Si ocurre, se pierde al usuario más influyente durante el cierre del piloto.
  - [PENDIENTE: definir plan de contingencia ante salida de Roberto Sánchez antes de octubre 2026; responsable: SPONSOR, antes del kick-off. Este plan debe incluir la redefinición del criterio cualitativo de aceptación documentada en §6.]
- **Laura Gómez:** licencia de maternidad programada para febrero 2027 — fuera del período crítico del proyecto. Riesgo bajo.

### Condiciones de entrada al proyecto (prerrequisitos)

1. Fuente de verdad declarada formalmente en reunión de kick-off (SPONSOR + Laura + Gerente de Compras presentes). Si no hay acuerdo en esa reunión, el proyecto no arranca.
2. Alineación del CEO aprobada para comprometer presupuesto.
3. Validación de acceso real a las tablas de SAP B1 (semana 1) — sin acceso verificado, no hay proyecto.

### Restricciones presupuestales

- Rango interno: COP 150 a COP 300 millones hasta diciembre 2026 (pendiente aprobación CEO). Por encima de COP 300M requiere aprobación de junta.
- Plazo de ejecución: **año fiscal 2026 inamovible** — sin posibilidad de arrastrar partidas a 2027.
- Riesgo de reasignación: si el proyecto no arranca antes de junio, el presupuesto puede ser reasignado en la revisión de mitad de año de julio.
- Principal costo: tiempo de Carlos (70-80% de su capacidad durante los primeros 4 meses). Servicios Azure: entre COP 8 y COP 15 millones mensuales estimados.

---

## 8. ARQUITECTURA TÉCNICA Y ALCANCE

### Alcance del piloto (v1)

- **Bodegas:** Bogotá, Medellín y Cali (3 bodegas que concentran el 70% del volumen).
- **Portafolio:** 300 SKUs tipo A; post-auditoría, 210-230 SKUs con historial limpio reciben el modelo principal; los 70-90 SKUs restantes (historia insuficiente, problema severo de devoluciones, quiebre prolongado) reciben modelo de fallback (promedio móvil ajustado por estacionalidad) etiquetado como "forecast de baja confianza" en el dashboard.
- **Criterio de extensión al resto del portafolio:** validación exitosa en el subconjunto piloto durante las 6 semanas de prueba.

### Elementos explícitamente fuera del alcance v1

1. Optimización de rutas.
2. Gestión de contratos con proveedores.
3. Planeación de promociones (las promociones entran como input, no se planean).
4. Reposición inter-bodega (extensión natural para v2).
5. Forecasting para canal e-commerce.
6. Generación automática de órdenes de compra en SAP.
7. Descuentos por acuerdo comercial (excepto descuentos de canal moderno en contratos físicos — Carlos evalúa viabilidad de digitalizarlos).

### Fuentes de entrada al modelo (con mecanismo de carga)

| Fuente | Mecanismo en v1 |
|--------|----------------|
| Datos históricos de demanda por SKU-bodega | Extracción SQL desde SAP B1 vía servidor de reporting; pipeline automatizado dominical; staging en Azure Data Lake |
| Excel de promociones de canal moderno | [PENDIENTE: si estructura del Excel es consistente, carga semanal manual por Carlos; si es inconsistente, se pospone a v2 y se modela con variables calendario únicamente. Ver nota de alineación SPONSOR-TECNICO en §5.] |
| Temporadas altas (4 eventos) | Variables calendario codificadas por Carlos; fechas estables sin fuente externa |
| Precios de lista | Tablas SAP B1 |
| Lead time de proveedores | Parámetro de configuración del modelo: 12-18 días (promedio portafolio); puede parametrizarse por segmento de proveedor |

### Salida del sistema (formato, acceso y permisos)

- **Dashboard de planeadores:** Power BI; forecast por SKU-bodega a 4 y 8 semanas; alertas de quiebre a 15 días; sugerencia de orden; tres drivers del forecast en lenguaje operativo; comparación forecast modelo vs. forecast ajustado por override.
- **Vista ejecutiva:** mismo workspace de Power BI, reporte separado con permisos distintos; capital de trabajo proyectado y fill rate esperado por categoría para CFO y Gerente de Compras.
- **Disponibilidad del dato:** lunes antes de las 7am (no negociable — el hábito de adopción se forma o se rompe en las primeras semanas del piloto).

### Arquitectura técnica

```
SAP B1 (SQL Server — servidor de reporting, solo lectura, horario nocturno)
    ↓ extracción SQL parametrizada (domingos en la noche)
Azure Data Lake Storage (capa de staging — tabla plana demanda diaria SKU-bodega)
    ↓ transformación y entrenamiento en Python (pandas + framework de forecasting)
Azure ML (ejecución del pipeline; evaluación de alternativa más ligera post-piloto)
    ↓ publicación de resultados
Azure SQL Database (resultados del modelo + tabla de overrides; evaluación de Azure Blob Storage post-piloto)
    ↓ conexión Power BI
Power BI (dashboard planeadores + vista ejecutiva)
```

> **[CRA-02 — CONDICIÓN]** La arquitectura de 5 capas descrita arriba está especificada sobre el Supuesto crítico 1 (acceso real a las tablas de SAP B1 con el nivel de detalle necesario). Este supuesto no ha sido validado con credenciales reales. Los documentos downstream (SAD, BDD) que hereden esta arquitectura deben marcar explícitamente la Sección 8 como "pendiente de validación de Supuesto 1 — semana 1 del proyecto". Si el acceso a SAP falla o las tablas tienen estructura diferente a la asumida, la arquitectura completa requiere revisión antes de comprometer recursos de desarrollo.

### Mecanismo de override y registro

Tabla de overrides en Azure SQL Database con campos: SKU, semana, forecast original del modelo, forecast ajustado, motivo en texto libre. Interfaz de entrada: **Power App embebida en el dashboard de Power BI** — el planeador abre el formulario desde Power BI y registra el ajuste sin salir del entorno. Power BI muestra ambos valores en paralelo. El forecast ajustado alimenta la recomendación de orden; el forecast original siempre queda visible para comparación y aprendizaje.

**[PENDIENTE: confirmar compatibilidad móvil de Power Apps para este caso de uso — requisito no negociable de Laura: el override debe registrarse desde cualquier dispositivo (celular, sala de reuniones) en el momento de la decisión, no en desktop horas después. Validación técnica: Carlos, semana 1 del proyecto. Si la validación confirma incompatibilidad móvil de Power Apps, debe definirse un plan B antes de comprometer la arquitectura de override. La funcionalidad de override mobile se considera entregable comprometido condicionado a esta validación técnica.]**

### Política de fallo del pipeline

**Decisión pendiente:** ante fallo del servidor SAP el domingo en la noche, el dashboard debe mostrar el forecast de la semana anterior con una etiqueta visible de "datos no actualizados" — nunca una pantalla en blanco. Una pantalla en blanco el lunes a las 7am genera pérdida de confianza inmediata. Esta política debe acordarse con el SPONSOR antes del inicio de la construcción.

### Monitoreo del pipeline en producción

Azure Monitor con alerta automática a Carlos y a Laura si el pipeline falla antes de las 6am del lunes. Sin componente de observabilidad no puede lanzarse a producción.

### Supuestos técnicos críticos (identificados por Carlos Méndez)

- **Supuesto crítico 1 (condición de entrada):** las tablas de SAP B1 son accesibles con el nivel de detalle necesario para construir la serie de demanda diaria por SKU-bodega. No validado con credenciales reales. Debe verificarse en la **semana 1 del proyecto** antes de comprometer el diseño del pipeline. Sin este supuesto validado, no hay proyecto.
- **Supuesto crítico 2 (riesgo de transferencia):** el equipo de BI tiene capacidad real para absorber el mantenimiento operativo post-enero 2027. Juan Diego asumió que sí, pero Carlos no ha hablado con ese equipo directamente. Ver Sección 9.
- Supuesto 3: tier actual de la suscripción Azure es suficiente para el volumen de datos y cómputo requeridos. Verificar en consola Azure antes de diseñar.
- Supuesto 4: el framework de forecasting elegido (Prophet u equivalente) corre sin conflictos en el entorno Azure ML; entorno de dependencias debe congelarse con requirements.txt o imagen Docker desde el día 1.
- Supuesto 5: workspace de Power BI en licencia Pro con frecuencia de refresco automático suficiente para el caso semanal.
- Supuesto 6: ver G2 — estructura del Excel de promociones.

### Decisiones técnicas requeridas antes del inicio de construcción

1. **Política de override (obligatoria antes de 1 septiembre):** confirmación de Power Apps como mecanismo + validación de compatibilidad móvil.
2. **Política de fallo del pipeline (obligatoria antes de 1 septiembre):** comportamiento ante fallo del servidor SAP en fin de semana.
3. **Presupuesto Azure SQL confirmado durante el piloto** (diferir evaluación de Azure Blob Storage a post-piloto).
4. **Evaluación de Azure ML vs. alternativa más ligera** (diferible a noviembre, con el modelo estabilizado).

---

## 9. TRANSFERENCIA Y SOSTENIBILIDAD

### Dueño operativo post-producción

**Laura Gómez** asume como dueña operativa del sistema a partir de enero 2027. Su rol: supervisión del uso, aprobación de cambios de configuración, escalar al equipo técnico cuando el modelo se degrada.

### Capacidad instalada requerida

El equipo de BI debe absorber el mantenimiento operativo del pipeline con capacidad de: (1) modificar parámetros del modelo, (2) reentrenarlo con datos nuevos, (3) diagnosticar fallos — sin necesidad de rediseñarlo desde cero. IT entra solo ante problemas de infraestructura Azure.

**[PENDIENTE: validar con el líder del equipo de BI su disponibilidad y familiaridad con el stack de Azure (Azure Data Factory, Python, Azure ML) antes del kick-off del proyecto. Si la capacidad es insuficiente, la transferencia de conocimiento requiere más tiempo y recursos del actualmente planificados. Responsable: SPONSOR + Carlos, antes del kick-off.]**

> **[CRA-04 — HIPÓTESIS NO VERIFICADA]** El plan de transferencia activa descrito en esta sección presupone que el equipo de BI tiene disponibilidad y familiaridad con el stack de Azure + Python. Esta es una hipótesis pendiente de validación con el líder del equipo de BI — no una decisión acordada. Si la validación confirma capacidad insuficiente, el plan de transferencia debe revisarse antes del kick-off y puede requerir recursos adicionales no presupuestados actualmente. Los documentos de arquitectura (SAD) deben marcar esta sección como condicional hasta que se complete la validación.

### Plan de transferencia

La transferencia de conocimiento es activa durante el desarrollo — no un entregable de cierre. Carlos incorpora al analista de BI designado desde las fases de construcción del pipeline para que aprenda haciendo, no leyendo documentación al final.

**Criterio de fracaso de transferencia:** si en enero 2027 el sistema solo puede ser mantenido por Carlos, el proyecto no terminó bien.

### Entregables de documentación obligatorios (prerrequisitos para la entrega final)

1. **Documentación técnica del pipeline y modelo** para el equipo de BI: arquitectura completa, decisiones de diseño con justificación, cómo reentrenar el modelo, cómo diagnosticar fallos del pipeline.
2. **Guía de usuario del dashboard** para planeadores: cómo interpretar el forecast, cómo registrar un override, qué hacer cuando el modelo falla o no actualiza.
3. **Documento de criterios de monitoreo del modelo** para Laura: cuándo el modelo se degrada, qué métricas observar (MAPE, tasa de intervención), cuándo escalar al equipo técnico.

Formato de documentación sin estándar corporativo establecido — Carlos define el formato con validación del SPONSOR.

### Lecciones aprendidas del episodio del ERP (patrones a evitar)

1. **No presentar soluciones terminadas:** los planeadores participan en revisiones intermedias desde el análisis exploratorio, no solo al recibir el producto final.
2. **No prometer granularidad que el modelo no puede cumplir:** si el modelo no funciona bien en algún SKU o bodega específica, se comunica explícitamente desde el inicio. El dashboard debe indicar el nivel de confianza del forecast por SKU.
3. **No desaparecer como sponsor:** el SPONSOR se compromete a revisión mensual con Laura y Carlos y disponibilidad para decisiones de alcance durante todo el proyecto. No solo la firma del kick-off.
4. **No ignorar señales tempranas de resistencia:** el plan de gestión de cambio tiene tres escalones y actúa desde la semana 1, no espera a que el rechazo se consolide.
