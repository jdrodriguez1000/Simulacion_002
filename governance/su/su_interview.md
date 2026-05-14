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

## FASE 2 — Confirmación y profundización

### 2.1 — Restricciones de tiempo y contexto [COMPLETADO 2026-05-14 10:05]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**2.1.a — Fecha límite para producción:**

Para impactar el fill rate de diciembre necesitamos el modelo en producción antes del 1 de septiembre de 2026. Esa es la fecha límite real porque los planeadores necesitan al menos 3 meses de uso para que las órdenes influenciadas por el modelo se reflejen en el inventario disponible en diciembre. Hay una fecha de corte adicional: el cierre del presupuesto de compras Q4 se hace en la primera semana de octubre — si el modelo no está operando antes de eso, los planeadores harán ese ejercicio sin él y perderemos un ciclo completo.

**2.1.b — Alineación con el CEO:**

La alineación con el CEO es un prerrequisito para comprometer presupuesto, pero no para iniciar. Podemos arrancar en paralelo con actividades que no requieran inversión: levantamiento de datos, análisis exploratorio, diseño de arquitectura. Si la reunión con el CEO resulta en un no, paramos. Si resulta en un sí con ajustes al alcance, los incorporamos.

**2.1.c — Eventos de negocio próximos:**

Tres eventos relevantes. Primero, la temporada de Día de la Madre ya pasó (10 de mayo) — los datos del pico estarán frescos en SAP y son útiles para validar el modelo. Segundo, la temporada de mitad de año (junio-julio) tiene un pico moderado por el Día del Padre y promociones de vacaciones escolares — sería un buen primer caso de prueba real si el modelo está listo para entonces. Tercero, en agosto hay una auditoría interna de procesos de Supply Chain que podría consumir tiempo de Laura y los planeadores durante 2-3 semanas.

---

### 2.2 — Criterios de éxito, umbrales y adopción [COMPLETADO 2026-05-14 10:20]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**2.2.a — Criterios de adopción y período de prueba:**

Habrá un período de prueba en paralelo de 6 semanas: los planeadores seguirán su proceso actual pero también verán las recomendaciones del modelo, y registrarán cuándo coinciden y cuándo difieren. La aceptación tiene dos componentes. Uno cuantitativo: el MAPE del forecast a 4 semanas debe ser inferior al 20% en los SKUs tipo A — ese es el umbral que se acordó con Carlos como técnicamente alcanzable y útil para el negocio. Uno cualitativo: Laura y Roberto deben declarar explícitamente que confían en usarlo como punto de partida. Si el número es bueno pero Roberto no confía, no hay adopción real. Ambos componentes son necesarios.

**2.2.b — Zona gris del fill rate:**

89% en diciembre no es fracaso ni éxito completo — es zona gris que requiere decisión. Criterio propuesto por el SPONSOR: si se llega a 89% o más, el proyecto continúa a fase 2 sin cuestionamiento. Si se llega entre 87% y 89%, se hace una revisión de causas antes de decidir continuidad. Si se queda por debajo de 87%, es un fracaso del proyecto. La autoridad para declarar fracaso es el SPONSOR, con input de Laura. El CEO entra solo si hay implicación presupuestaria de continuar o detener.

**2.2.c — Intervenciones manuales como métrica:**

Las intervenciones manuales de Roberto forman parte del criterio de éxito, pero no como restricción binaria. El sistema se considera exitoso en adopción si los planeadores lo usan como punto de partida aunque lo corrijan. Métrica a seguir: tasa de intervención. Expectativa en las primeras 6 semanas: 40% o más de las recomendaciones intervenidas — se considera normal. Si a los 6 meses la tasa de intervención sigue por encima del 30% en SKUs tipo A, es señal de que el modelo no está aprendiendo o hay variables no capturadas.

**2.2.d — Autoridad para pasar a producción:**

La decisión de pasar de prueba a producción la toma el SPONSOR, con aval explícito de Laura. El Gerente de Compras debe ser informado pero no tiene veto. El CEO no necesita aprobar ese paso. Lo que sí requeriría escalar al CEO es si durante la prueba el alcance cambia significativamente o el presupuesto se excede.

---

### 2.3 — Dependencias, disponibilidad y riesgos operativos [COMPLETADO 2026-05-14 10:45]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**2.3.a — Dependencias de IT y datos:**

1. El acceso al servidor de reporting requiere un proceso formal: Carlos debe enviar una solicitud a IT con el visto bueno del SPONSOR por correo. IT la procesa en 5-10 días hábiles y asigna credenciales de solo lectura. Este trámite debe iniciarse desde el primer día del proyecto.
2. SAP B1 tiene una ventana de mantenimiento planificada en la primera semana de julio — actualizan el servidor de reporting en ese mismo período. Downtime estimado de 2 días. No es un bloqueo crítico pero hay que evitar extracciones masivas en esa semana.

**2.3.b — Disponibilidad durante la prueba:**

1. La auditoría de agosto consume a Laura aproximadamente el 60% de su tiempo durante 2-3 semanas. No puede participar activamente en la prueba al mismo tiempo. Recomendación del SPONSOR: iniciar la prueba piloto la última semana de agosto, con 5 semanas de prueba en paralelo hasta la primera semana de octubre. Eso queda justo para el cierre de presupuesto Q4.
2. En septiembre hay una feria sectorial de logística donde Laura y el Gerente de Compras participan durante 3 días. Reduce disponibilidad esa semana pero no es bloqueante para la prueba.

**2.3.c — Política de fuente de verdad:**

El SPONSOR tiene la autoridad para declarar la fuente de verdad y está dispuesto a hacerlo, pero necesita hacerlo con Laura y el Gerente de Compras presentes en la sala — no por encima de ellos. Se formalizará en la reunión de kick-off del proyecto, antes de que Carlos acceda a los datos. Si se llega al kick-off sin ese acuerdo, el proyecto no arranca. Es una condición de entrada, no un supuesto.

**2.3.d — Riesgos de continuidad:**

1. Carlos Méndez (TECNICO): sin planes de salida conocidos. Riesgo bajo.
2. Laura Gómez (USUARIO): licencia de maternidad programada para febrero de 2027 — fuera del período crítico del proyecto. Riesgo bajo para el período de prueba.
3. Roberto Sánchez (planeador senior, usuario clave): riesgo más real. Tiene conversaciones internas sobre una posible promoción a coordinador regional que lo sacaría del equipo de planeación. Probabilidad estimada baja para antes de octubre, pero no es cero. Si ocurre, se pierde al usuario más influyente justo antes del cierre del año. No hay plan de contingencia para ese escenario actualmente.

---

### 2.4 — Alcance, límites del sistema e integraciones [COMPLETADO 2026-05-14 11:00]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**2.4.a — Alcance geográfico y de portafolio:**

Piloto focalizado: 3 bodegas principales (Bogotá, Medellín y Cali) que concentran el 70% del volumen, y los 300 SKUs tipo A. Una vez validado el modelo en ese subconjunto, se extiende al resto. Lanzar con 12 bodegas y 1.800 SKUs desde el inicio es un riesgo innecesario.

**2.4.b — Límites del sistema:**

Los cinco elementos están todos fuera de v1: (1) optimización de rutas, (2) gestión de contratos con proveedores, (3) gestión de promociones (solo input, no planeación), (4) reposición inter-bodega (extensión natural para v2), (5) forecasting para e-commerce. Límite adicional explícito: el modelo no genera órdenes de compra directamente en SAP, solo recomendaciones. La entrada en SAP la hace el planeador manualmente. No negociable en v1.

**2.4.c — Fuentes de datos que entran al modelo:**

El Excel de promociones del área comercial entra como input desde v1 — demasiado importante para SKUs tipo A donde las promociones pueden duplicar la demanda. Carlos define un proceso liviano de carga semanal de ese Excel hasta que exista integración formal. Las 4 temporadas las modela Carlos como variables calendario codificadas — fechas conocidas y estables, sin fuente externa. Precios de lista en SAP entran como variable. Descuentos por acuerdo comercial quedan fuera de v1, excepto descuentos de canal moderno (en contratos físicos) — Carlos evalúa si vale la pena digitalizarlos.

**2.4.d — Integraciones de salida:**

Dashboard construido sobre Power BI — infraestructura ya existe, planeadores ya tienen licencias. Carlos construye datasets y transformaciones; equipo de BI apoya con diseño de vistas. Recomendaciones de orden no se conectan a SAP en v1 — el planeador las ve en Power BI y las entra manualmente (intencional, para construir confianza). El CFO y el Gerente de Compras necesitan vista agregada separada (capital de trabajo proyectado y fill rate esperado por categoría) — mismo workspace de Power BI pero reporte diferente y permisos separados.

---

### 2.5 — Arquitectura técnica y modelo [COMPLETADO 2026-05-14 11:15]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**2.5.a — Plataforma cloud:**

Suscripción activa de Microsoft Azure contratada hace 18 meses para otros proyectos de analytics. IT ya aprobó ese entorno para datos de la compañía y tiene los acuerdos de seguridad firmados. Salir de Azure requeriría un proceso de aprobación de seguridad que tomaría meses. Carlos trabajará en Azure — no está en discusión.

**2.5.b — Frecuencia de actualización:**

Semanal es suficiente para v1. Proceso schedulado automáticamente los domingos en la noche, resultados listos el lunes a las 7am. Si el proceso falla, debe haber alerta automática a Carlos y a Laura antes de las 6am del lunes. No puede depender de ejecución manual.

**2.5.c — Restricción de interpretabilidad:**

No se limita a modelos lineales. Carlos puede usar XGBoost o LightGBM si el dashboard muestra, para cada SKU, los tres principales drivers del forecast esa semana — explicación a nivel de predicción individual (no solo feature importances globales). Ejemplo: "la demanda proyectada es alta principalmente por proximidad a temporada de Navidad y por incremento en ventas de las últimas 3 semanas". No hay restricción regulatoria ni de auditoría.

**2.5.d — Arquitectura de datos:**

Tres capas: (1) extracción desde SAP hacia Azure Data Lake Storage, (2) transformación y entrenamiento en Azure ML, (3) publicación de resultados hacia dataset de Power BI vía Azure SQL Database. Carlos diseña y construye el pipeline. Mantenimiento operativo post-producción lo asume el equipo de BI con soporte de Carlos para cambios en el modelo. IT solo entra si hay problemas de infraestructura en Azure.

**2.5.e — Mecanismo de override:**

Funcionalidad que Carlos debe diseñar explícitamente — no edición directa en Power BI (se necesita trazabilidad). Tabla de overrides en Azure SQL Database donde el planeador registra: SKU, semana, forecast original del modelo, forecast ajustado, y motivo en texto libre. Power BI muestra ambos valores en paralelo. El forecast ajustado alimenta la recomendación de orden; el forecast original siempre queda visible. Permite comparar sistemáticamente dónde el modelo se equivoca vs. dónde Roberto se equivoca — alimenta iteraciones de mejora.

---

### 2.6 — Gestión del cambio y comunicación [COMPLETADO 2026-05-14 11:30]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**2.6.a — Plan de comunicación y lanzamiento:**

Comunicación en dos fases: primero reunión privada con Laura y Roberto antes del kick-off (co-diseño del mecanismo de override — que sientan que son parte del diseño, no receptores de solución impuesta). Dos semanas después, presentación general al equipo. Narrativa deliberada: "el modelo aprende de su experiencia — cada vez que ustedes lo corrigen, se vuelve más inteligente". No se habla de eficiencia ni reducción de tiempo inicialmente (activa miedo a ser reemplazados). Para Roberto: necesita ver una demo con datos de sus propios SKUs antes del piloto, no datos genéricos.

**2.6.b — Capacitación y onboarding:**

Responsabilidad de Carlos con apoyo de Laura. Formato: dos sesiones de 2 horas con casos reales del negocio, no presentaciones teóricas. Tiempo máximo: 4 horas de capacitación formal más práctica durante las 5 semanas de prueba. La herramienta debe ser suficientemente intuitiva para que el onboarding ocurra durante el uso. Campeón interno: Andrés Torres, planeador de bebidas, 2 años en el equipo, perfil analítico, ya usa tablas dinámicas avanzadas y ha preguntado espontáneamente sobre machine learning.

**2.6.c — Gestión de la resistencia activa:**

Estrategia en tres escalones: (1) primeras dos semanas — Laura tiene conversación directa mostrando datos de intervenciones vs. modelo; (2) semana tres — SPONSOR tiene conversación uno a uno con Roberto; (3) semana cinco — si Roberto sigue bloqueando activamente y otros lo siguen, decisión ejecutiva: continúa piloto con Andrés como referente principal y se gestiona situación de Roberto por separado con RRHH. Punto de no retorno: si Roberto influye activamente para que otros planeadores no usen la herramienta.

**2.6.d — Comunicación hacia arriba:**

Reporte al CEO solo en hitos clave (kick-off confirmado, modelo en prueba piloto, resultado de diciembre). Si algo sale mal entre hitos, se comunica proactivamente. Narrativa para fill rate insuficiente por razones externas: separar desempeño del modelo (precisión del forecast, adopción) del desempeño del negocio (fill rate con otras variables). Esta distinción se establece desde el kick-off con el CEO para que no sea sorpresa en diciembre.

---

### 2.7 — Presupuesto y restricciones financieras [COMPLETADO 2026-05-14 11:45]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**2.7.a — Presupuesto disponible:**

No está formalmente aprobado — la aprobación ocurre en la reunión con el CEO la próxima semana. Rango interno: COP 150 a COP 300 millones para todo el proyecto hasta diciembre de 2026 (incluye infraestructura Azure, tiempo de Carlos y componentes externos menores). Por encima de COP 300 millones requeriría aprobación de junta, lo que alargaría los tiempos significativamente.

**2.7.b — Distribución de la inversión:**

Mayor costo: tiempo de Carlos (70-80% de su capacidad durante los primeros 4 meses). Servicios Azure estimados entre COP 8 y COP 15 millones mensuales. Sin consultoría externa (aprendizaje del episodio del ERP). Sin presupuesto formal para change management más allá del tiempo interno de Laura y Carlos. Si se identifica necesidad de apoyo externo durante el proyecto, se escala al CEO.

**2.7.c — Base de la aprobación:**

La ecuación de ROI existe internamente (construida por Carlos y el SPONSOR) pero no ha sido presentada formalmente a la junta. La aprobación del CEO se basará principalmente en el argumento estratégico: fill rate como objetivo de la compañía y riesgo de perder contratos de canal moderno. El ROI se usa como respaldo si preguntan, no como argumento principal.

**2.7.d — Restricciones fiscales y contables:**

Presupuesto debe ejecutarse en año fiscal 2026 — no hay posibilidad de arrastrar partidas a 2027. Si el proyecto no arranca antes de junio, la ventana de ejecución se acorta y el presupuesto puede ser reasignado en la revisión de mitad de año de julio. Umbral de licitación formal: COP 200 millones en un solo contrato con proveedor externo — no aplica porque no hay contratos externos de ese tamaño. Servicios Azure se contratan a través del acuerdo corporativo existente.

---

### 2.8 — Definición de éxito, fracaso y transferencia [COMPLETADO 2026-05-14 12:00]

**Informante:** Juan Diego Rodriguez (SPONSOR)

**2.8.a — Declaración de éxito al cierre:**

El éxito tiene tres elementos definidos. (1) Fill rate sube de 87% a al menos 91% y los dos contratos de canal moderno están seguros. (2) Los planeadores usan el sistema todas las semanas porque les ayuda — adopción genuina, no forzada. (3) Capacidad instalada que no depende de Carlos como única persona con conocimiento del sistema. Si los tres elementos están presentes: éxito completo. Si el fill rate llega a 90% pero hay adopción genuina y pipeline estable, también es éxito. Lo que no puede venderse como éxito: un modelo técnicamente bueno que nadie usa.

**2.8.b — Condición de fracaso inapelable:**

Tres condiciones de parada. (1) Fill rate por debajo de 87% (ya definido en 2.2). (2) Si los datos de SAP tienen problemas de integridad tan severos que el modelo aprende sobre datos incorrectos y sus recomendaciones son peores que el criterio humano. (3) Si el equipo de planeación sabotea activamente el proyecto — intervenciones ficticias, datos incorrectos ingresados al sistema. Esa tercera condición es un problema organizacional, no de data science, y no puede resolverse con más iteraciones del modelo.

**2.8.c — Transferencia y sostenibilidad:**

Dueño operativo a partir de enero de 2027: Laura Gómez, con soporte técnico del equipo de BI para el pipeline. Carlos debe dejar al menos un analista de BI con capacidad de: (1) modificar parámetros del modelo, (2) reentrenarlo con datos nuevos, (3) diagnosticar fallos — sin necesidad de rediseñarlo desde cero. La transferencia de conocimiento debe ocurrir de forma activa durante el desarrollo, no al final como entregable de cierre. Criterio de fracaso de transferencia: si en enero de 2027 el sistema solo puede ser mantenido por Carlos, el proyecto no terminó bien.

**2.8.d — Gestión del conocimiento y documentación:**

Tres entregables obligatorios antes de la entrega final: (1) Documentación técnica del pipeline y modelo para equipo de BI — arquitectura, decisiones de diseño, cómo reentrenar. (2) Guía de usuario del dashboard para planeadores — cómo interpretar el forecast, cómo registrar un override, qué hacer cuando el modelo falla. (3) Documento de criterios de monitoreo del modelo para Laura — cuándo el modelo se degrada, qué métricas observar, cuándo escalar. Sin estándar corporativo para este tipo de documentación; Carlos define el formato con validación del SPONSOR. La documentación es prerrequisito para la entrega final, no un artefacto post-cierre.

**2.8.e — Lecciones del ERP y compromisos del sponsor:**

Cuatro patrones del episodio del ERP que no deben repetirse: (1) No presentar soluciones terminadas — los planeadores participan en revisiones intermedias desde el análisis exploratorio. (2) No prometer granularidad que el modelo no puede cumplir — si no funciona bien en algún SKU o bodega, se dice explícitamente desde el inicio. (3) No desaparecer como sponsor — el SPONSOR se compromete a revisión mensual con Laura y Carlos y a estar disponible para decisiones de alcance. (4) No ignorar señales tempranas de resistencia. Compromiso explícito del SPONSOR: atención real, no solo firma en el kick-off.

---

## FASE 2 — COMPLETADA [2026-05-14 12:00]

Todas las secciones 2.1 a 2.8 capturadas. Informante principal: Juan Diego Rodriguez (SPONSOR).


