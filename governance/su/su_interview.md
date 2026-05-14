# SU Interview — Documento de entrevista
**Proyecto:** [A confirmar en sección 1.1]
**Fecha de inicio:** 2026-05-14
**Agente:** su_interviewer

---

## FASE 0 — Mapa de stakeholders [COMPLETADO 2026-05-14 09:15]

| Rol | Nombre | Cargo | Disponibilidad |
|-----|--------|-------|----------------|
| SPONSOR | Juan Diego Rodriguez | Director de Data & Analytics | Disponible como punto de contacto principal |
| TECNICO | Carlos Méndez | Data Scientist Senior | Tiempo completo durante el proyecto |
| USUARIO | Laura Gómez | Jefe de Cadena de Suministro | Martes y jueves, 1 hora por sesión |

**Informante:** Juan Diego Rodriguez (SPONSOR)

---

## FASE 1 — Exploración del problema

### 1.1 — Contexto organizacional y del problema [COMPLETADO 2026-05-14]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**1.1.a — ¿Cuál es la organización, industria y área involucrada en este proyecto?**

Somos la unidad de Data & Analytics de una empresa distribuidora de consumo masivo en Colombia. Operamos a nivel nacional con presencia en 12 ciudades. El área de Supply Chain tiene aproximadamente 40 personas entre planeadores, analistas de inventario y coordinadores de compras. La industria es distribución y logística de productos de consumo masivo.

**1.1.b — ¿Cuál es el problema concreto que quieren resolver?**

Hoy los planeadores deciden cuándo y cuánto pedir a los proveedores basándose en su experiencia personal y en reportes estáticos de Excel. Esto genera dos problemas frecuentes: quiebres de stock en productos de alta rotación que frenan las ventas, y sobrestock en productos de baja rotación que inmoviliza capital. No tenemos una forma sistemática de anticipar la demanda futura por SKU.

**1.1.c — ¿Cuándo empezó este problema y qué se ha intentado antes?**

El problema existe desde hace al menos 3 años. Se intentó resolver una vez con una consultoría externa que implementó un módulo de planeación en el ERP, pero los planeadores dejaron de usarlo porque los pronósticos eran muy agregados (a nivel de categoría, no de SKU) y no reflejaban la estacionalidad real del negocio. Desde entonces volvimos al Excel.

---

### 1.2 — Impacto del problema [COMPLETADO 2026-05-14 09:25]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**1.2.a — ¿Cómo miden el impacto del problema hoy?**

Seguimos dos métricas principales. Para quiebres de stock: tasa de fill rate al cliente, que hoy está en 87% cuando el objetivo es 95%. Estimamos que cada punto porcentual de fill rate perdido equivale a aproximadamente COP 800 millones en ventas no realizadas al año. Para sobrestock: días de inventario por categoría — hoy tenemos categorías con más de 90 días de inventario cuando el estándar del negocio es 45 días. El capital inmovilizado en exceso ronda los COP 12.000 millones.

**1.2.b — ¿Qué áreas de la organización están afectadas y cómo?**

Los planeadores son los más afectados operativamente: dedican cerca del 60% de su tiempo a apagar incendios reactivos en lugar de planear. El área comercial sufre los quiebres directamente porque pierden ventas y deterioran relaciones con clientes clave. Finanzas presiona por la inmovilización de capital. Y la Dirección General lo tiene como uno de los tres objetivos estratégicos del año.

**1.2.c — ¿Qué consecuencias tiene no resolver este problema en el corto plazo?**

Si no lo resolvemos este año, enfrentamos dos riesgos concretos: perder dos contratos con clientes de canal moderno que tienen cláusulas de fill rate mínimo del 93%, y no cumplir la meta de reducción de capital de trabajo que la junta directiva exige para el cierre fiscal de 2026. La presión es real y tiene fecha.

---

### 1.3 — Solución esperada y restricciones [COMPLETADO 2026-05-14 09:35]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**1.3.a — ¿Qué debe hacer la solución?**

El lunes por la mañana cada planeador debería abrir un dashboard y ver, por SKU y por bodega, tres cosas: el forecast de demanda para las próximas 4 y 8 semanas, una alerta de los SKUs que van a quiebra en los próximos 15 días si no se ordena, y una sugerencia de cantidad y fecha de orden considerando el lead time del proveedor. La decisión que debe volverse más rápida es precisamente esa: cuándo lanzar una orden de compra y por cuánto. Hoy eso les toma medio día por categoría; debería tomar 30 minutos para toda su cartera.

**1.3.b — ¿Cuáles son los criterios de éxito?**

A diciembre de 2026 (6 meses): fill rate subiendo de 87% a mínimo 91%, días de inventario bajando de 90 a 65 días en las categorías críticas, y los planeadores usando el sistema — métrica proxy: al menos 80% de las órdenes de compra generadas ese mes referenciando el forecast del modelo. A mayo de 2027 (12 meses): fill rate en 95% sostenido por dos meses consecutivos, días de inventario en 45 días, y los dos contratos de canal moderno renovados sin penalización por fill rate.

**1.3.c — ¿Cuáles son las restricciones?**

Cuatro restricciones no negociables. Primero, debe integrarse con el ERP actual (SAP B1) para leer inventario y movimientos — no podemos pedir extracciones manuales, ya quemamos esa credibilidad. Segundo, los planeadores deben poder ver y entender por qué el modelo recomienda lo que recomienda — nada de caja negra, aprendimos eso con la consultoría anterior. Tercero, el equipo de IT no tiene capacidad para mantener infraestructura nueva, así que la solución debe correr en la nube con mínima intervención de su parte. Cuarto, presupuesto acotado: no podemos adquirir licencias de software adicionales de costo significativo.

---

### 1.4 — Stakeholders y política organizacional [COMPLETADO 2026-05-14 09:45]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**1.4.a — Actores clave:**

Tenemos 8 planeadores en total, organizados por categoría de producto: 3 cubren alimentos, 2 bebidas, 2 cuidado del hogar y 1 cuidado personal. Existe un Coordinador de Planeación — ese es el cargo de Laura Gómez — que revisa y consolida antes de que salgan las órdenes. Además de los planeadores, el Gerente de Compras necesita ver los outputs agregados para negociar volúmenes con proveedores, y el CFO quiere visibilidad del capital de trabajo proyectado.

**1.4.b — Proceso de aprobación:**

El planeador genera la propuesta de orden, Laura la revisa y aprueba órdenes hasta COP 50 millones. Por encima de ese monto entra el Gerente de Compras. El sistema debe producir la recomendación y dejar la decisión final al planeador — no debe generar órdenes automáticamente. Laura es explícita en ese punto: quiere que el modelo sea un copiloto, no un autopiloto.

**1.4.c — Resistencias:**

Hay dos planeadores con más de 8 años de antigüedad que son los más escépticos. Su argumento es que "el negocio tiene muchas variables que un modelo no puede capturar", refiriéndose a promociones y negociaciones especiales. Con el ERP hubo un factor político importante: la consultoría implementó el módulo sin involucrar a los planeadores en el diseño, se los presentaron terminado y les pidieron que confiaran. Eso generó rechazo activo. El planeador con más antigüedad, Roberto Sánchez, tiene influencia sobre el equipo — si él no adopta, los demás tampoco. Lo que necesita Roberto para dar su apoyo es poder intervenir el forecast manualmente cuando su criterio difiera del modelo, y que esa intervención quede registrada para aprender de ella.

**1.4.d — Patrocinador ejecutivo:**

El SPONSOR (Juan Diego Rodriguez) es el sponsor directo del proyecto. Su jefe es el CEO, quien tiene visibilidad general del objetivo estratégico de mejorar el fill rate, pero no del proyecto de forecasting específicamente. Alineación del CEO pendiente — agendada para la próxima semana antes de iniciar el desarrollo.

---

### 1.5 — Datos disponibles y acceso a sistemas [COMPLETADO 2026-05-14 10:00]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**1.5.a — Historial de ventas:**

Historial de ventas por SKU y por bodega en SAP B1 desde 2019, aproximadamente 6 años de datos. Las 12 bodegas están registradas como centros de costo separados. El historial de movimientos de inventario también está en SAP B1: entradas, salidas, traslados entre bodegas.

**1.5.b — Calidad de los datos:**

SAP B1 es la fuente oficial pero tiene problemas conocidos. Entre 2020 y 2021 hubo una migración parcial que dejó aproximadamente 4 meses con registros incompletos. Algunos planeadores registran devoluciones de clientes con códigos incorrectos, lo que distorsiona las salidas reales. Los planeadores confían más en sus Excel propios para productos de alta rotación: hojas de seguimiento semanal que consideran más confiables que los reportes de SAP. Necesidad identificada: establecer SAP como fuente de verdad o reconciliar ambas fuentes antes de entrenar el modelo.

**1.5.c — Promociones y eventos:**

Las promociones de canal moderno (supermercados) están en contratos físicos y en un Excel del área comercial; no integradas a SAP. Las promociones de canal tradicional son informales y en muchos casos solo las conoce el ejecutivo de ventas de zona. Cuatro temporadas altas identificadas: Navidad, Semana Santa, regreso a clases y Día de la Madre — conocidas por el equipo pero no formalmente documentadas en ningún sistema centralizado.

**1.5.d — Portafolio de SKUs:**

Aproximadamente 1.800 SKUs activos. Clasificación ABC básica en SAP: SKUs tipo A son alrededor de 300 y representan el 80% de las ventas. Rotación moderada del portafolio: entran y salen entre 80 y 120 SKUs por año, principalmente en la categoría de cuidado personal.

**1.5.e — Conexión a SAP B1:**

Existe conexión de lectura utilizada por el equipo de BI para reportes en Power BI mediante consultas directas a la base de datos SQL Server del backend de SAP B1. Canal abierto y aprobado por IT. Condición: cualquier conexión nueva debe ser de solo lectura y pasar por el servidor de reporting, no conectarse directamente al servidor productivo de SAP.

---

## FASE 1 — COMPLETADA [2026-05-14 10:00]

Todas las secciones 1.1 a 1.5 capturadas. Informante principal: Juan Diego Rodriguez (SPONSOR).

---

