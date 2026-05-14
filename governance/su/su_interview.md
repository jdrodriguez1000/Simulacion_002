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

---

## FASE 2.T — Entrevista técnica [COMPLETADO 2026-05-14 12:30 - EN CURSO]

### 2.T.1 — Estructura y volumen de datos [COMPLETADO 2026-05-14 13:00]

**2.T.1.a — Confiabilidad del histórico en SAP B1: análisis crítico**

**Pregunta:** En términos de volumen, ¿cuál es realmente el histórico confiable que puedes usar para entrenar el modelo? Más allá de los 6 años nominales que mencionó Juan Diego, ¿cuál es tu estimación realista en meses de datos usables por SKU tipo A?

**Respuesta:** Siendo honesto: si entreno hoy con lo que hay en SAP B1 sin trabajo previo de limpieza, el historial confiable promedio por SKU es de aproximadamente 28 a 32 meses — no 6 años. Esto por tres razones acumuladas.

La migración de 2020-2021 elimina efectivamente 4 meses de historia para la mayoría de SKUs, y para algunos productos que se relanzaron en ese período el historial pre-migración no es comparable con el post-migración — no son la misma serie de tiempo.

Los códigos de devolución incorrectos afectan principalmente los SKUs de alta rotación, que paradójicamente son los más importantes para el modelo. Hasta que no hagamos una reconciliación con los Excel de los planeadores, no puedo cuantificar exactamente el sesgo, pero mi estimación conservadora es que entre el 8% y el 15% de las salidas registradas en SAP para SKUs tipo A tienen ruido por este problema.

El tercer factor es la distribución por antigüedad del portafolio: de los 300 SKUs tipo A, aproximadamente 60 fueron introducidos después de 2022 y tienen menos de 3 años de historia. Para esos SKUs necesito estrategias diferentes — cold start con datos de productos similares o modelos más simples mientras acumulan historia.

Mi recomendación antes de tocar el modelo: dedicar las primeras 3 semanas del proyecto exclusivamente a auditoría y limpieza de datos. Sin eso, cualquier número de MAPE que reporte será sobre datos sucios y no será reproducible en producción.

**Informante:** Carlos Méndez (TECNICO)

**2.T.1.b — Formato, acceso y pipeline de extracción**

**Pregunta:** ¿Cómo accedes exactamente a esos datos? ¿Qué formato tienen, cuál es el patrón de acceso que usarás?

**Respuesta:** El servidor de reporting expone las tablas de SAP B1 directamente vía SQL Server — no hay una capa de abstracción intermedia ni cubos OLAP. El equipo de BI ya hace queries directas a ese servidor para alimentar sus reportes de Power BI, así que el patrón de acceso está establecido y yo puedo replicarlo.

Las tablas relevantes para el modelo son conocidas en el ecosistema SAP B1: OITM para maestro de productos, OINM para movimientos de inventario, ORDR y RDR1 para órdenes de venta, y OPOR/POR1 para órdenes de compra. El problema es que SAP B1 no fue diseñado para queries analíticas — las tablas están normalizadas para transacciones, no para series de tiempo. Construir la serie de demanda diaria por SKU y bodega requiere joins no triviales y lógica de negocio para distinguir salidas reales de devoluciones, traslados inter-bodega y ajustes de inventario.

Mi plan de extracción es escribir queries SQL parametrizadas que generen una tabla plana de demanda diaria por SKU-bodega, y persistir esa tabla en Azure Data Lake como capa de staging. Desde ahí trabajo en Python con pandas y posteriormente con las librerías de forecasting. No proceso directo desde SAP al modelo — siempre con capa intermedia para no repetir la extracción cada vez que reentreno.

Una advertencia adicional: el equipo de IT pidió que las queries no corran en horas pico del servidor de reporting — entre 7am y 6pm. La extracción semanal debe programarse en horario nocturno, lo que es perfectamente compatible con el schedule dominical que propuso Juan Diego.

**Informante:** Carlos Méndez (TECNICO)

**2.T.1.c — Estimación realista de SKUs tipo A con historial limpio y suficiente**

**Pregunta:** De los 300 SKUs tipo A, después de la auditoría y limpieza inicial, ¿cuántos puedo usar realmente para entrenar el modelo en v1 con confianza razonable?

**Respuesta:** Mi estimación realista después de las 3 semanas de auditoría: entre 210 y 230 SKUs tipo A con 24 meses o más de historial limpio y utilizable — eso es entre el 70% y el 77% de los 300 SKUs tipo A del piloto.

Los 70 a 90 SKUs restantes caen en tres categorías problemáticas. Unos 60 son productos introducidos después de 2022 con historia insuficiente. Unos 20 tienen el problema de devoluciones tan severo que la reconciliación con los Excel puede no ser suficiente para limpiarlos completamente. Y unos 10 a 15 estuvieron en quiebre de stock prolongado durante 2021-2022 — su historial existe pero está censurado, la demanda real no se observa porque no había producto disponible.

Mi recomendación para el entrenamiento inicial: arrancar con los 210 SKUs limpios, que representan aproximadamente el 85% del volumen de ventas de los SKUs tipo A. Los SKUs con historia insuficiente los manejo con un modelo de fallback más simple — promedio móvil ajustado por estacionalidad — y los etiqueto explícitamente en el dashboard para que los planeadores sepan que esos forecasts son menos confiables. No los excluyo del sistema, pero sí soy transparente sobre la calidad de la predicción. Eso también abona a la credibilidad con Roberto — mejor decir 'este SKU tiene forecast de baja confianza' que presentar un número con falsa precisión.

**Informante:** Carlos Méndez (TECNICO)

### 2.T.1 — Estructura y volumen de datos [COMPLETADO 2026-05-14 13:15]

---

### 2.T.2 — Calidad y completitud [EN PROGRESO]

**2.T.2.a — Períodos con datos incompletos o de menor calidad [COMPLETADO 2026-05-14 14:15]**

**Pregunta:** En el histórico que revisaste, ¿hay períodos específicos donde los datos podrían estar incompletos, con menor calidad, o donde simplemente el nivel de cobertura o consistencia cambia de forma notoria?

**Respuesta:** Identifico cinco períodos con señales de alerta que documentaré formalmente durante la auditoría:

Marzo–junio 2020: inicio de pandemia. Las ventas tuvieron comportamiento atípico extremo — quiebres masivos en algunas categorías y sobredemanda en otras. Ese período existe en SAP pero no es representativo de la demanda normal del negocio. Lo incluiré en el entrenamiento pero con una variable indicadora de anomalía para que el modelo no aprenda ese patrón como estacional.

Octubre 2020–febrero 2021: migración de SAP. Como mencioné, 4 meses con registros incompletos. Para los SKUs afectados voy a imputar con interpolación donde sea posible, y donde no, voy a truncar el historial y usar solo datos post-migración — prefiero menos datos limpios que más datos sucios.

Diciembre 2021–enero 2022: hubo un problema logístico nacional por paro de transportadores que afectó los despachos durante 3 semanas. Las salidas de SAP de ese período reflejan restricción de oferta, no demanda real. Necesito confirmación de Laura sobre las fechas exactas para enmascarar ese período.

Semanas de inventario cero por SKU: dispersos a lo largo de toda la serie. Son los períodos de quiebre de stock que mencioné — la demanda observada es cero pero la demanda real no lo era. Voy a usar los datos de órdenes de venta rechazadas o pendientes de SAP para intentar reconstruir la demanda latente donde sea posible.

Datos de 2019: el año más antiguo tiene menor granularidad en algunos registros — sospecho que el SAP anterior al actual tenía configuraciones diferentes. Lo usaré con cautela y lo excluiré si durante la auditoría confirmo inconsistencias estructurales.

En resumen: el historial realmente utilizable sin intervención especial es 2022-2025. Todo lo anterior requiere tratamiento explícito caso a caso.

**Informante:** Carlos Méndez (TECNICO)

---

**2.T.2.b — Estrategia de imputación y tratamiento de datos faltantes [COMPLETADO 2026-05-14 14:35]**

**Pregunta:** De esos períodos problemáticos, ¿cuál es tu estrategia específica de imputación o exclusión? ¿Hay períodos que definitivamente no usarás, y hay períodos donde intentarás reconstruir datos usando métodos estadísticos o datos externos?

**Respuesta:** Trabajo con tres niveles de tratamiento según la naturaleza del problema:

**Exclusión definitiva — sin intento de recuperación:**
Los 4 meses de migración SAP (octubre 2020–febrero 2021) para SKUs con registros incompletos superiores al 40% de las semanas del período. No vale la pena imputar cuando la mayoría del período está ausente — el riesgo de introducir sesgo sistemático es mayor que el beneficio de tener más historia. Esos SKUs simplemente arrancan su serie en marzo 2021.

**Enmascaramiento con variable indicadora — incluyo pero controlo:**
Marzo–junio 2020 (pandemia) y diciembre 2021–enero 2022 (paro transportadores). Los datos existen y están en SAP pero son atípicos. Los incluyo en el entrenamiento con una variable binaria de 'período anómalo' para que el modelo aprenda a ignorarlos como patrón recurrente. Esta estrategia es preferible a excluirlos porque algunos modelos de series de tiempo se desestabilizan cuando hay saltos temporales en la serie.

**Reconstrucción activa — intento recuperar demanda real:**
Períodos de quiebre de stock donde la demanda observada es cero pero la demanda real existía. Aquí tengo dos fuentes posibles para reconstruir: primero, las órdenes de venta en SAP que quedaron pendientes o fueron rechazadas durante el quiebre — esas representan demanda insatisfecha documentada. Segundo, para SKUs donde no hay órdenes pendientes, usaré interpolación basada en el comportamiento de SKUs similares de la misma categoría que no tuvieron quiebre en el mismo período. No es perfecta pero es mejor que dejar ceros que el modelo interpretará como demanda real nula.

**2019 — decisión diferida a la auditoría:**
No tomo decisión sobre 2019 hasta revisar los datos. Si la auditoría confirma inconsistencias estructurales, lo excluyo completamente. Si los datos son comparables con períodos posteriores, los incluyo con variable indicadora de 'año base antiguo'. No comprometo esa decisión antes de ver los datos.

**Aclaración metodológica importante:** Toda decisión de imputación o exclusión queda documentada en un data lineage log — qué se modificó, por qué, y qué impacto tiene en el volumen de entrenamiento. Eso es no negociable para mí tanto por reproducibilidad técnica como porque Laura y Roberto van a preguntar por qué el modelo no usa todos los datos disponibles.

**Informante:** Carlos Méndez (TECNICO)

---

**2.T.2.c — Plan concreto de coordinación con Laura para validación de datos [COMPLETADO 2026-05-14 14:50]**

**Pregunta:** Teniendo en cuenta todo lo anterior, ¿cuál es el plan operativo concreto que necesitas de Laura durante esas 3 semanas de auditoría? ¿Sesiones continuas, puntuales, qué exactamente?

**Respuesta:** Necesito tres cosas concretas de Laura antes de que arranquen mis 3 semanas de auditoría, no durante:

Primero — documento de eventos operativos históricos:
Necesito que Laura o alguien de su equipo prepare una línea de tiempo de eventos que hayan distorsionado la demanda normal desde 2019: paros, quiebres masivos, lanzamientos de productos, discontinuaciones, cambios de precio significativos, promociones de alto impacto. No tiene que ser exhaustivo ni formal — un Excel con fecha de inicio, fecha de fin y descripción breve es suficiente. Esto me toma a mí semanas de inferencia estadística; a Laura le toma probablemente dos horas de memoria institucional. Necesito ese documento antes del día uno de la auditoría.

Segundo — acceso a los Excel de los planeadores:
Necesito los archivos de seguimiento semanal de los planeadores de los últimos 24 meses, específicamente los de los SKUs tipo A. No necesito que los preparen ni los limpien — los recibo como están. Con eso puedo hacer la reconciliación de devoluciones comparando las salidas que registraron ellos versus lo que quedó en SAP. Solicito que Laura centralice esos archivos antes del inicio de la auditoría — si los pido planeador por planeador durante la auditoría pierdo días enteros en coordinación.

Tercero — dos sesiones de validación durante la auditoría:
Una sesión al final de la semana uno — 90 minutos — donde le presento a Laura los hallazgos preliminares de calidad de datos y ella confirma o corrige mis interpretaciones de los períodos problemáticos. Una segunda sesión al final de la semana tres — 60 minutos — donde revisamos juntos la decisión final sobre qué datos entran al entrenamiento y ella da su aval formal. Esa segunda sesión es crítica: si Laura no aprueba las decisiones de tratamiento de datos, cualquier cuestionamiento posterior al modelo lo vamos a rastrear hasta aquí.

Fuera de esas dos sesiones y la preparación previa, no necesito más tiempo de Laura durante la auditoría. Sé que tiene carga operativa y no puedo pedirle disponibilidad continua.

**Informante:** Carlos Méndez (TECNICO)

### 2.T.2 — Calidad y completitud [COMPLETADO 2026-05-14 14:50]

---

### 2.T.3 — Viabilidad técnica de la arquitectura propuesta [EN PROGRESO]

**2.T.3.a — Viabilidad general de la arquitectura y puntos de fricción [COMPLETADO 2026-05-14 15:05]**

**Pregunta:** La arquitectura propuesta por Juan Diego (SAP → Azure Data Lake → Azure ML → Power BI vía Azure SQL) — ¿es viable en general? ¿Hay aspectos que funcionarán bien, y hay aspectos que requieren decisiones explícitas antes de comprometer recursos?

**Respuesta:** La arquitectura es viable y es la correcta para este contexto — Azure, Power BI ya en uso, IT con capacidad limitada. Pero hay cinco puntos de fricción que necesito que queden documentados ahora porque van a aparecer durante el desarrollo:

**Punto 1 — Azure ML puede ser sobredimensionado:**
Para este volumen de datos — 300 SKUs, series semanales, reentrenamiento semanal — Azure ML Managed Endpoints puede ser más infraestructura de la necesaria. Una Azure Function o un simple Azure Container Instance schedulado puede ejecutar el pipeline de reentrenamiento con menor costo y menor complejidad de mantenimiento. Propongo evaluar esto durante el diseño técnico antes de comprometer la arquitectura. Si Juan Diego aprobó el presupuesto con Azure ML en mente, lo uso, pero quiero que sea una decisión consciente no una suposición.

**Punto 2 — Azure SQL Database tiene implicación de costo:**
Azure SQL Database tiene costo fijo mensual aunque no se use intensivamente. Para el volumen de este proyecto, una alternativa más económica sería Azure Blob Storage con archivos Parquet que Power BI lee directamente vía conector — cero costo de base de datos. Nuevamente, decisión de diseño que debe tomarse explícitamente.

**Punto 3 — La tabla de overrides necesita escritura, no solo lectura:**
La arquitectura como está descrita es de solo lectura desde SAP hacia Power BI. Pero el mecanismo de override de Roberto requiere que los planeadores escriban datos desde Power BI hacia alguna capa de almacenamiento. Power BI no tiene escritura nativa — necesitamos un formulario externo, una Power App embebida, o una entrada manual en Azure SQL. Esto no está resuelto en la arquitectura actual y es funcionalidad crítica.

**Punto 4 — Monitoreo del pipeline en producción:**
No hay componente de observabilidad definido. Si el pipeline falla el domingo en la noche, ¿cómo se detecta antes de las 7am del lunes? Necesito definir alertas — Azure Monitor o algo más simple — desde el inicio, no como mejora futura.

**Punto 5 — El servidor de reporting de SAP como punto único de falla:**
Toda la arquitectura depende de que ese servidor esté disponible el domingo en la noche. Si SAP tiene mantenimiento no planificado o el servidor está lento, el pipeline falla. Necesito una estrategia de retry y una política de qué mostrar en Power BI cuando el dato no se actualiza — ¿el forecast de la semana anterior con una etiqueta de advertencia, o una pantalla de error?

Ninguno de estos cinco puntos es bloqueante, pero todos requieren decisión explícita antes de que empiece a construir.

**Informante:** Carlos Méndez (TECNICO)

---

**2.T.3.b — Priorización de puntos de fricción y plan de resolución [COMPLETADO 2026-05-14 15:25]**

**Pregunta:** De esos cinco puntos, ¿cuál es el más crítico que debe estar resuelto antes del 1 de septiembre? ¿Cuáles pueden diferirse post-piloto? ¿Y cuál es tu plan específico para cada uno?

**Respuesta:** El más crítico es el Punto 3 — mecanismo de override con escritura. Es el único de los cinco que bloquea funcionalidad que Juan Diego declaró no negociable: Roberto necesita poder intervenir el forecast y que esa intervención quede registrada. Sin eso no hay adopción, y sin adopción no hay proyecto. Los otros cuatro puntos son de arquitectura o costo — importantes pero no bloquean el valor central del sistema.

Mi recomendación específica para resolverlo antes del 1 de septiembre: implementar una Power App embebida en el dashboard de Power BI. El planeador ve el forecast, abre el formulario, registra el override y el motivo, y la Power App escribe directamente a una tabla en Azure SQL Database. Es la solución más rápida de implementar, no requiere desarrollo web personalizado, y los planeadores ya tienen licencias de Microsoft 365 que incluyen Power Apps. Tiempo de implementación estimado: 1 semana una vez definido el modelo de datos.

Clasificación completa antes del 1 de septiembre vs. post-piloto:

**Antes del 1 de septiembre — obligatorio:**
- **Punto 3 (override con escritura):** bloqueante de adopción, resuelvo con Power Apps.
- **Punto 4 (monitoreo del pipeline):** no puedo lanzar producción sin alerta de fallo dominical. Implemento Azure Monitor con un alert rule simple — medio día de trabajo.
- **Punto 5 (política de fallo del servidor SAP):** necesito definir el comportamiento ante fallo antes del piloto para no sorprender a los planeadores el primer lunes que el dato no aparezca. Decisión de diseño más que desarrollo — 1 hora con Juan Diego para acordar la política, luego lo implemento.

**Post-piloto — diferible sin riesgo:**
- **Punto 1 (Azure ML vs. alternativa más ligera):** durante el piloto puedo correr el pipeline en Azure ML sin problema. La optimización de costo y complejidad la hago en noviembre cuando tengamos el modelo estabilizado y sepamos el patrón real de uso.
- **Punto 2 (Azure SQL vs. Blob Storage):** mismo argumento — el costo incremental durante el piloto es bajo y no vale la pena el riesgo de cambiar la arquitectura de publicación justo antes de que los planeadores empiecen a usarla. Lo evalúo para la versión de producción definitiva en diciembre.

**Resumen ejecutivo para Juan Diego:** necesito tres decisiones tuyas antes de que empiece a construir — la política de override, la política de fallo del pipeline, y confirmación del presupuesto para Azure SQL durante el piloto. Las demás las resuelvo yo.

**Informante:** Carlos Méndez (TECNICO)

---

**2.T.3.c — Supuestos técnicos no validados y riesgos residuales [COMPLETADO 2026-05-14 15:45]**

**Pregunta:** De los cinco puntos de fricción que mencionaste, ¿hay supuestos técnicos aún no validados que si fallan tendrían impacto significativo en el proyecto? ¿Cuáles son los supuestos más críticos que necesitan validación antes de comprometer el presupuesto?

**Respuesta:** Identifico seis supuestos técnicos que sostienen la solución y que aún no han sido validados. Si alguno falla, el impacto va desde retraso hasta rediseño parcial.

**Supuesto 1 — Las tablas de SAP B1 son accesibles con el nivel de detalle que necesito:**
Asumo que puedo construir una serie de demanda diaria por SKU-bodega desde las tablas SQL de SAP. No lo he verificado con credenciales reales. SAP B1 tiene versiones y configuraciones que afectan qué tablas existen y qué campos están poblados. Si IT configuró el servidor de reporting con vistas limitadas en lugar de tablas completas, mi plan de extracción cambia. Esto debe validarse en la primera semana del proyecto, antes de comprometer el diseño del pipeline.

**Supuesto 2 — El volumen de datos es manejable con el tier de Azure que tenemos:**
No conozco el tier actual de la suscripción Azure de la empresa. Para 1.800 SKUs con historia de 6 años el volumen de datos bruto es manejable — estimado bajo 10 GB — pero si el tier de Azure ML o Azure SQL Database es básico, puede haber limitaciones de cómputo o almacenamiento. Necesito acceso a la consola de Azure para verificar antes de diseñar.

**Supuesto 3 — Prophet o el framework de forecasting elegido corre sin conflictos en el entorno Azure:**
Prophet tiene dependencias de compilación que en Windows a veces generan problemas. Azure ML corre en Linux por defecto lo que reduce ese riesgo, pero si el equipo de BI necesita reproducir el entorno localmente en Windows para mantenimiento, puede haber fricción. Debo definir el entorno de dependencias desde el día uno y congelarlo con un requirements.txt o imagen Docker.

**Supuesto 4 — Power BI tiene capacidad de refresco automático suficiente:**
Si el workspace de Power BI actual está en licencia Pro, el refresco automático está limitado a 8 veces por día — suficiente para nuestro caso semanal. Pero si en el futuro queremos aumentar frecuencia, necesitamos Premium. No es un riesgo para v1 pero debo confirmarlo para no encontrar límites inesperados durante el piloto.

**Supuesto 5 — El equipo de BI tiene capacidad real para mantener el pipeline post-enero 2027:**
Juan Diego asumió que el equipo de BI absorbe el mantenimiento operativo. No he hablado con ese equipo directamente. Si tienen carga alta o no tienen familiaridad con Azure Data Factory o el stack que voy a usar, la transferencia de conocimiento requiere más tiempo del que está planificado. Recomiendo una conversación explícita con el líder del equipo de BI antes del kick-off para confirmar disponibilidad y alinear expectativas.

**Supuesto 6 — Los datos de promociones del Excel comercial tienen estructura consistente:**
Asumo que ese Excel tiene un formato estable semana a semana que puedo parsear automáticamente. Si cada analista comercial lo llena diferente o cambia columnas frecuentemente, el proceso de carga semanal se convierte en mantenimiento manual continuo. Necesito ver ese archivo antes de comprometer que entra como input en v1 — si la estructura es caótica, lo muevo a v2 y en v1 lo capturo solo como variable calendar de temporadas conocidas.

**Condición de entrada que recomiendo formalizar antes de la aprobación del proyecto:**
Los supuestos 1 y 5 son los más críticos. El supuesto 1 porque sin acceso verificado a los datos no hay proyecto. El supuesto 5 porque si el equipo de BI no puede absorber el mantenimiento, Carlos sigue siendo dueño indefinidamente y eso es un riesgo organizacional que Juan Diego necesita conocer antes de comprometer el presupuesto.

**Informante:** Carlos Méndez (TECNICO)

### 2.T.3 — Viabilidad técnica de la arquitectura propuesta [COMPLETADO 2026-05-14 15:45]

---

## FASE 2.T — Entrevista técnica [COMPLETADO 2026-05-14 15:45]

### CIERRE FORMAL DE FASE 2.T

**Fecha de conclusión:** 2026-05-14 15:45

**Duración total:** 2 horas 45 minutos (13:00-15:45)

**Entrevistado:** Carlos Méndez, Data Scientist Senior (TECNICO)

**Hallazgos clave por sección:**

#### 2.T.1 — Estructura y volumen de datos
- **Histórico realmente confiable:** 28-32 meses promedio por SKU tipo A (no 6 años)
- **SKUs tipo A utilizables tras auditoría:** 210-230 de 300 (70-77%)
- **Recomendación crítica:** 3 semanas obligatorias de auditoría y limpieza antes de entrenamiento
- **Implicación:** el volumen de entrenamiento es menor del estimado, pero más confiable

#### 2.T.2 — Calidad y completitud
- **Períodos problemáticos identificados:** 5 períodos con anomalías documentadas (2020 pandemia, 2020-2021 migración SAP, 2021-2022 paro transportadores, quiebres de stock dispersos, 2019 datos antiguos)
- **Estrategia de tratamiento:** Exclusión definitiva para datos incompletos >40%, enmascaramiento con variables indicadoras para anomalías, reconstrucción activa para demanda censurada
- **Requerimiento operativo:** necesita documento de eventos históricos de Laura + acceso a Excel de planeadores + 2 sesiones de validación de 90 y 60 minutos
- **Implicación:** La calidad de datos requiere trabajo activo coordinado antes de entrenar

#### 2.T.3 — Viabilidad técnica
- **Arquitectura general:** viable, pero 5 puntos de fricción identificados
- **Punto crítico bloqueante:** mecanismo de override con escritura (Punto 3) — necesario para adopción
- **Resolución recomendada:** Power Apps embebida en dashboard, 1 semana de implementación
- **Decisiones ejecutivas requeridas antes del 1 de septiembre:**
  - Aprobación de Punto 3 (override con Power Apps)
  - Definición de política ante fallo del pipeline SAP
  - Confirmación de presupuesto Azure SQL durante piloto
- **Diferibles post-piloto:** optimización de costo (Azure ML vs. alternatives), arquitectura de publicación (SQL vs. Blob Storage)

#### 2.T.3 — Supuestos técnicos críticos
- **6 supuestos identificados, 2 críticos antes de aprobación:**
  1. **Supuesto 1 (Acceso SAP):** debe validarse semana 1 del proyecto — SIN ESTE NO HAY PROYECTO
  2. **Supuesto 5 (Capacidad equipo BI para mantenimiento):** debe acordarse con líder BI antes del kick-off — riesgo organizacional de dependencia de Carlos indefinida
- **4 supuestos adicionales:** volumen Azure, framework de forecasting, capacidad Power BI, estructura Excel promociones — validables durante primeras semanas sin bloquear inicio

### Gaps y riesgos documentados para síntesis:

1. **Validación de acceso SAP** — condición de entrada crítica
2. **Capacidad de equipo BI post-enero 2027** — riesgo de transferencia de conocimiento
3. **Estructura del Excel de promociones** — determina si entra en v1 o se pospone a v2
4. **Mecanismo de override** — requiere decisión arquitectónica antes del 1 de septiembre
5. **Política de fallo del pipeline** — debe estar definida antes del piloto para no sorprender en producción

### Información técnica lista para síntesis:
- Historial de datos realmente utilizable y plan de auditoría
- Estrategia de tratamiento de datos con lineage documentado
- Arquitectura viable con puntos de fricción prorizados
- Identificación de supuestos críticos vs. diferibles
- Ruta clara hacia decisiones ejecutivas en pre-kick-off

---

## FASE 2.U — Entrevista con Laura Gómez (USUARIO) [EN PROGRESO]

**Contexto de Fase 2.U:**
Laura Gómez es la Jefe de Cadena de Suministro y Coordinadora de Planeación. Su rol es crucial para validar el contexto de uso diario del sistema de forecasting y los pain points operativos que el modelo debe resolver. Esta fase captura la perspectiva del usuario final que usará el sistema semana a semana.

**Disponibilidad:** Martes y jueves, 1 hora por sesión (confirmada en Fase 0)

**Duración sesión estimada:** 45 minutos

### 2.U.1 — Contexto de uso diario [EN PROGRESO]

**2.U.1.a — Flujo de trabajo típico del lunes [COMPLETADO 2026-05-14 16:10]**

**Pregunta:** Describe tu flujo de trabajo típico desde que llegas el lunes a la oficina. ¿Qué haces primero, cuánto tiempo te toma cada paso, dónde están los principales cuellos de botella o puntos de fricción?

**Respuesta:** El lunes empieza antes de llegar a la oficina. Generalmente reviso en el celular los mensajes del equipo comercial del fin de semana — si hubo algún quiebre o urgencia durante el sábado, ya llego con esa información.

Al llegar, lo primero que hago es abrir el reporte de inventario que uno de mis planeadores extrae de SAP cada lunes a primera hora. Ese reporte tarda entre 45 minutos y una hora en generarse porque SAP no tiene un reporte estándar que nos sirva — el planeador hace la extracción, la pega en un Excel maestro y aplica las fórmulas que hemos construido durante años. Ese Excel es lo que realmente usamos para tomar decisiones, no SAP directamente.

Con ese Excel abierto, hago un recorrido por categorías. Reviso días de inventario por SKU, identifico los que están por debajo del punto de reorden que definimos empíricamente, y marco los que necesitan orden urgente. Ese recorrido me toma entre una y dos horas dependiendo de cuántos SKUs estén en zona crítica.

Luego cada planeador trabaja de forma independiente su categoría — propone las órdenes de compra, define cantidades basándose en su criterio y en el historial que conocen de memoria, y me manda un resumen para revisión. Ese proceso les toma entre dos y cuatro horas por planeador.

A media tarde consolido las propuestas, las reviso contra el presupuesto disponible de compras, ajusto donde hay conflicto de capital y apruebo. Las órdenes que superan mi límite las escalo al Gerente de Compras. Normalmente cerramos las decisiones de la semana entre las 4 y las 6 de la tarde del lunes.

El problema real es que ese flujo asume que todo sale bien. Cuando hay una urgencia — un cliente llamando por un quiebre, un proveedor que no entregó — el proceso se fragmenta y terminamos tomando decisiones de reorden a las 8 de la noche con información incompleta.

**Informante:** Laura Gómez (USUARIO)

---

**2.U.1.b — Frecuencia y patrones de eventos disruptivos [COMPLETADO 2026-05-14 16:25]**

**Pregunta:** ¿Con qué frecuencia ocurren esas interrupciones o eventos inesperados que te sacan del plan? ¿Hay días o momentos específicos de la semana donde esto es más probable?

**Respuesta:** Siendo realista: no existe la semana sin interrupciones. Lo que varía es la intensidad.

En una semana normal — que diría que es el 40% de las semanas — hay entre dos y tres interrupciones menores. Un proveedor que avisa que entregará tarde, un cliente que reclama un faltante puntual, un planeador que descubre que el inventario físico no cuadra con SAP. Esas las resolvemos dentro del horario normal sin mayor impacto en la planeación.

En una semana complicada — que es el otro 60% — hay al menos una interrupción mayor que consume entre dos y cuatro horas del día: un quiebre imprevisto en un SKU tipo A, un rechazo de mercancía en bodega, una promoción que el área comercial activó sin avisarnos con anticipación. Esas semanas son las que terminan con decisiones de reorden nocturnas.

El miércoles y el jueves son los días más vulnerables. El lunes cerramos las órdenes de la semana, pero para el miércoles ya están llegando las entregas de proveedores con lead time corto y es cuando se revelan los faltantes reales versus lo que esperábamos. El jueves es cuando el área comercial consolida sus resultados de ventas de la semana y nos pide reaccionar.

El efecto acumulado es que la planeación proactiva — pensar en las próximas cuatro semanas — ocurre en la práctica solo los lunes por la mañana, antes de que empiecen las urgencias. Si ese tiempo se reduce por cualquier razón, tomamos decisiones de reorden casi completamente reactivas. Eso es lo que más me preocupa del modelo actual: no es que no sepamos planear, es que el sistema operativo no nos da el espacio para hacerlo.

**Informante:** Laura Gómez (USUARIO)

### 2.U.1 — Contexto de uso diario [COMPLETADO 2026-05-14 16:25]

---

## 2.U.2 — Pain points y expectativas [EN PROGRESO]

### 2.U.2.a — Pain points operativos más agudos [COMPLETADO 2026-05-14 16:45]

**Pregunta:** De todo lo que has descrito — los quiebres de stock, los reorders nocturnos, las interrupciones de miércoles y jueves — ¿cuál es el problema que más te quita el sueño operativamente? ¿Cuál es el que, si lo resolvieras, tendría el mayor impacto en tu trabajo día a día?

**Respuesta:** Sin dudar: no saber con anticipación suficiente qué va a quebrar.

Hoy cuando identifico que un SKU está en riesgo de quiebre, en la mayoría de los casos ya es demasiado tarde para reaccionar bien. El lead time promedio de nuestros proveedores es de 12 a 18 días. Si el lunes detecto que un SKU tipo A va a quebrar en 10 días, ya no tengo margen — el pedido llega cuando el quiebre ya ocurrió o está ocurriendo. Termino negociando entregas parciales urgentes a mayor costo, o peor, llamando al cliente para pedirle paciencia.

Lo que me quitaría el sueño sería tener esa visibilidad con cuatro o seis semanas de anticipación. No necesito que el modelo sea perfecto — necesito que me diga con suficiente tiempo de anticipación 'este SKU va a tener problema' para que yo pueda actuar dentro de los tiempos normales del negocio, sin urgencias ni sobrecostos.

El segundo problema en importancia es la asimetría de información con el área comercial. Ellos activan promociones y negocian volúmenes especiales sin coordinación sistemática con nosotros. Cuando nos enteramos, el inventario ya no alcanza. Pero ese problema no lo resuelve un modelo de forecasting solo — requiere un cambio de proceso entre dos áreas. Lo menciono porque si el modelo consume los datos de promociones del Excel comercial como input, ya estaríamos dando el primer paso para formalizar esa coordinación.

Si tuviera que elegir uno solo: la anticipación en quiebres. Eso cambia completamente la naturaleza de mi trabajo — paso de apagar incendios a gestionar riesgos. Esa diferencia para mí es enorme, no solo en resultados sino en calidad de vida del equipo.

**Informante:** Laura Gómez (USUARIO)

---

**2.U.2.b — Transformación del flujo de trabajo con forecast a 4-6 semanas [COMPLETADO 2026-05-14 16:50]**

**Pregunta:** Si tuvieras el forecast de demanda disponible el lunes por la mañana — con visibilidad de 4 a 6 semanas — ¿cómo cambiaría tu día laboral? ¿Qué te quitaría de encima y qué nuevas actividades podrías hacer que hoy casi no haces?

**Respuesta:** El lunes cambiaría fundamentalmente en un punto: dejaría de ser un día de diagnóstico y se convertiría en un día de decisiones.

Hoy el lunes lo paso descubriendo el estado del inventario — extrayendo datos, construyendo el Excel, identificando qué está en zona crítica. Eso me consume la mañana. Con el forecast disponible, llegaría el lunes sabiendo ya qué SKUs van a tener problema en las próximas cuatro a seis semanas. El dashboard me lo mostraría ordenado por urgencia. No tendría que buscar el problema — el problema vendría a mí.

Lo que cambiaría en concreto: en lugar de revisar los 300 SKUs tipo A para encontrar los 20 que están en riesgo, empezaría directamente con esos 20 priorizados. Eso me libera entre una y dos horas de la mañana. Ese tiempo lo invertiría en algo que hoy casi nunca hago: revisar las causas detrás del riesgo y coordinar con el área comercial antes de lanzar la orden — ¿hay una promoción planificada que justifica pedir más?, ¿hay un cambio de proveedor que afecta el lead time?, ¿conviene consolidar esta orden con otra que ya está pendiente?

Para los planeadores el cambio sería similar. Hoy llegan y construyen su diagnóstico. Con el forecast llegarían con el diagnóstico hecho y usarían su criterio — que es valioso — para validar, ajustar y decidir, no para descubrir. Roberto en particular: su experiencia de 8 años no desaparece, se aplica mejor. Él sabría cosas que el modelo no sabe — una negociación especial con un proveedor, un cliente que está a punto de hacer un pedido grande — y ese conocimiento lo incorporaría vía el override de forma estructurada en lugar de quedarse solo en su cabeza.

Una cosa adicional que cambiaría y que nadie ha mencionado: las conversaciones con el Gerente de Compras. Hoy cuando le escalo una orden grande, la conversación es reactiva — 'necesitamos esto urgente'. Con forecast de seis semanas, la conversación sería 'en seis semanas vamos a necesitar este volumen, ¿negociamos condiciones ahora?'. Eso tiene valor económico directo — mejores precios, mejores condiciones de entrega — que hoy no estamos capturando porque siempre llegamos tarde.

**Informante:** Laura Gómez (USUARIO)

---

**2.U.2.c — Restricciones de tiempo y contexto de uso [COMPLETADO 2026-05-14 16:55]**

**Pregunta:** Teniendo en cuenta tu flujo de trabajo el lunes y los eventos de urgencia durante la semana — ¿hay restricciones de tiempo, contexto o dispositivo que el sistema DEBE respetar para ser útil en tu día a día?

**Respuesta:** Hay tres restricciones reales que el sistema debe respetar:

Primera — el dato debe estar listo antes de las 7am del lunes:
No a las 8, no a las 9. Los planeadores llegan entre 7 y 7:30, y si el dashboard no tiene datos frescos al llegar, la primera reacción es volver al Excel de siempre. El hábito se forma o se rompe en esas primeras semanas. Si el lunes llegan y el sistema no tiene datos, ese día trabajamos con el método antiguo y perdemos confianza. Carlos mencionó las 7am — eso es correcto y es innegociable.

Segunda — las decisiones de override deben poder registrarse en el momento, desde cualquier dispositivo:
Cuando estoy en una reunión con el Gerente de Compras y surge una decisión sobre un SKU específico, necesito poder registrar ese ajuste en ese momento desde el celular o desde la sala de reuniones. No puedo volver a mi escritorio dos horas después a recordar qué decidí y por qué. Si el mecanismo de override solo funciona bien en desktop, vamos a tener subregistro — los planeadores van a tomar decisiones que no quedan documentadas. Eso arruina el aprendizaje del modelo y la trazabilidad que Juan Diego necesita.

Tercera — el sistema debe funcionar aunque SAP esté caído:
Los viernes en la tarde y algunos sábados IT hace mantenimientos no programados en SAP. Si el pipeline depende de que SAP esté disponible ese fin de semana, el lunes puede amanecer sin datos actualizados. La política de fallback que Carlos mencionó no es opcional — necesitamos que el dashboard muestre el forecast de la semana anterior con una etiqueta clara de 'datos no actualizados' antes que una pantalla en blanco. Una pantalla en blanco el lunes a las 7am genera pánico innecesario.

Hay un contexto de uso diferente al lunes típico que vale mencionar: los jueves en la tarde, cuando consolidamos urgencias de la semana, también consultamos el sistema para ver si las decisiones de reorden del lunes fueron suficientes o si hay que ajustar. Ese uso es secundario — no necesita datos frescos, solo los del lunes — pero el sistema debe estar disponible y estable durante toda la semana, no solo el lunes.

**Informante:** Laura Gómez (USUARIO)

---

**2.U.2.d — Criterios de fracaso y situaciones donde volvería a Excel [COMPLETADO 2026-05-14 17:15]**

**Pregunta:** En el extremo opuesto — ¿hay situaciones concretas donde dirías "esto no está funcionando, volvemos al Excel"? ¿Qué condiciones o fallos de la herramienta te harían abandonarla?

**Respuesta:** Hay cuatro situaciones concretas donde dejaría de usar el sistema:

Primera — si el modelo me falla en los SKUs más importantes sin explicación:
Si un lunes el modelo proyecta demanda normal para un SKU tipo A y tres semanas después ese SKU quiebra, necesito entender por qué falló. Si la única respuesta que obtengo es un número diferente la semana siguiente sin ninguna explicación de qué cambió, pierdo confianza rápidamente. No exijo que el modelo sea perfecto, pero sí exijo que cuando se equivoca sea transparente sobre por qué. Un modelo que falla en silencio es peor que el Excel, porque al menos en el Excel yo sé exactamente qué asumí.

Segunda — si el tiempo de adopción supera el beneficio percibido en las primeras semanas:
El sistema debe mostrar valor visible en las primeras dos o tres semanas del piloto. Si después de un mes los planeadores sienten que están haciendo más trabajo — registrando overrides, validando datos, aprendiendo una herramienta nueva — sin ver que sus decisiones mejoran, volvemos al Excel. El valor tiene que ser perceptible rápido. No en diciembre — en octubre.

Tercera — si el dashboard requiere interpretación experta para usarse:
Si los planeadores necesitan entender estadística para interpretar lo que ven, el sistema no sirve para este equipo. Tengo planeadores muy buenos operativamente que no tienen formación analítica avanzada. Si el dashboard muestra intervalos de confianza, percentiles o métricas técnicas sin traducirlas a lenguaje operativo — 'este SKU tiene alto riesgo de quiebre en 3 semanas', no 'el percentil 80 del forecast supera el inventario proyectado' — lo van a ignorar.

Cuarta — si el sistema no respeta las excepciones del negocio:
Hay SKUs con comportamientos que ningún modelo va a capturar bien inicialmente: productos con demanda intermitente, SKUs que solo se mueven por pedidos especiales de un cliente específico, productos en proceso de discontinuación. Si el modelo genera recomendaciones de reorden para esos SKUs como si fueran productos normales, los planeadores van a perder confianza en todo el sistema, no solo en esos SKUs. Necesitamos una forma de marcar excepciones — 'este SKU no se pronostica con el modelo general' — desde el inicio, no después de que el error ya ocurrió.

El denominador común de los cuatro escenarios es el mismo: si el sistema me hace sentir que estoy sirviendo a la herramienta en lugar de que la herramienta me sirva a mí, vuelvo al Excel sin dudar.

**Informante:** Laura Gómez (USUARIO)

### 2.U.2 — Pain points y expectativas [COMPLETADO 2026-05-14 17:15]

---

## FASE 2.U — Entrevista con Laura Gómez (USUARIO) [COMPLETADO 2026-05-14 17:15]

### CIERRE FORMAL DE FASE 2.U

**Fecha de conclusión:** 2026-05-14 17:15

**Duración total:** 1 hora 5 minutos (16:10-17:15)

**Entrevistado:** Laura Gómez, Jefe de Cadena de Suministro (USUARIO)

**Hallazgos clave por sección:**

#### 2.U.1 — Contexto de uso diario
- **Flujo típico del lunes:** Diagnóstico de estado inventario (45 min a 1 hora de extracción SAP), revisión de riesgo por SKU (1-2 horas), propuestas de planeadores (2-4 horas), consolidación y aprobación (2-4 horas). Cierre de decisiones entre 4-6 pm.
- **Patrón de interrupciones:** 40% de semanas normales (2-3 interrupciones menores), 60% de semanas complicadas (1+ interrupción mayor de 2-4 horas). Picos de vulnerabilidad: miércoles (entregas de proveedores revelan faltantes) y jueves (consolidación de ventas del área comercial).
- **Actividad de planeación proactiva:** Ocurre solo los lunes por la mañana antes de urgencias — si ese tiempo se reduce, las decisiones se vuelven completamente reactivas.
- **Implicación para el sistema:** El lunes por la mañana es el punto crítico. Si el sistema no absorbe al menos la mitad del trabajo de diagnóstico de inventario, no hay beneficio real.

#### 2.U.2 — Pain points y expectativas
- **Pain point crítico:** Falta de visibilidad con anticipación de quiebres potenciales. Lead time de proveedores 12-18 días; si detecta riesgo con 10 días de anticipación, ya es tarde. Necesita 4-6 semanas de visibilidad.
- **Pain point secundario:** Asimetría de información con área comercial — promociones activadas sin coordinación sistemática. No lo resuelve solo el forecasting, pero intake del Excel comercial como input comienza la formalización.
- **Transformación esperada del flujo de trabajo:** Pasar de diagnóstico/descubrimiento a decisión/validación. Lunes cambiaría de 2-3 horas de búsqueda de problemas a 30 min de revisión de problemas priorizados. Tiempo liberado se invertiría en análisis de causas raíz y coordinación con Gerente de Compras.
- **Beneficio específico para planeadores:** Roberto podría aplicar su experiencia de 8 años de forma estructurada vía overrides, en lugar de dejarla solo en su cabeza. Su conocimiento no desaparece, se amplifica.
- **Restricciones operativas NO negociables (3):**
  1. Dato listo antes de 7am del lunes (no a las 8 ni a las 9) — hábito se forma o quiebra las primeras semanas
  2. Override debe funcionar desde cualquier dispositivo en el momento (celular, sala de reuniones) — si solo funciona en desktop hay subregistro y se pierde el aprendizaje del modelo
  3. Sistema debe funcionar aunque SAP esté caído (fallback a forecast anterior con etiqueta de advertencia, nunca pantalla en blanco)
- **Uso secundario:** Consultas los jueves en la tarde para validar si las decisiones de reorden del lunes fueron suficientes — no requiere datos frescos pero el sistema debe estar disponible toda la semana.
- **Criterios de fracaso (4 situaciones donde abandonaría):**
  1. **Fallos sin explicación en SKUs importantes:** Modelo falla silenciosa peor que Excel. Necesita transparencia de por qué cambió.
  2. **Tiempo adopción > beneficio en 2-3 semanas:** Debe mostrar valor visible rápido. Si después de un mes el equipo siente que hace MÁS trabajo sin mejora, vuelta a Excel.
  3. **Dashboard requiere expertise técnica:** Planeadores sin formación analítica no pueden interpretar intervalos, percentiles — necesita lenguaje operativo.
  4. **No respeta excepciones del negocio:** SKUs intermitentes, especiales, en discontinuación necesitan marcar DESDE EL INICIO, no post-error. Pérdida de confianza en TODO el sistema si trata excepciones como productos normales.
- **Denominador común de criterios de fracaso:** Si el sistema la hace servir a la herramienta en lugar de que la herramienta la sirva, vuelve al Excel sin dudar.

### Gaps y riesgos documentados para síntesis:

1. **Visibilidad SAP vs. Excel operativo:** Planeadores confían más en sus Excel que en SAP para productos críticos. Fuente de verdad debe resolverse antes de entrenar.
2. **Excepciones del negocio no catalogadas:** SKUs con comportamiento especial necesitan identificación y marcaje INICIAL — no es afterthought.
3. **Mecanismo de override mobile-friendly:** Debe ser usable desde celular en reuniones, no solo en desktop.
4. **Comunicación de incertidumbre del modelo:** Necesita poder explicar por qué falló cada predicción. Interpretabilidad es requisito operativo, no lujo.
5. **Captura del criterio de Roberto:** Sus 8 años de experiencia deben canalizarse vía override con motivo texto libre, auditable para aprendizaje del modelo.

### Información de usuario final lista para síntesis:
- Contexto operativo del flujo de trabajo lunes-semana con tiempos específicos
- Pain points concretos con métrica de impacto (lead time 12-18 días vs. visibility requerida 4-6 semanas)
- Transformación esperada del trabajo día a día (diagnóstico → decisión)
- Restricciones operativas NO negociables con justificación (3 restricciones, 1 uso secundario)
- Criterios de fracaso específicos y cómo el sistema puede evitarlos
- Énfasis crítico: control de usuario, no automatización de decisiones

