# SU Knowledge Gaps — Análisis de completitud del transcript
**Agente:** su_needs_analyzer
**Fecha:** 2026-05-14
**Complexity:** medium (cb_threshold=3)
**Umbral de aprobación:** confidence_score >= 0.80

---

## RESUMEN EJECUTIVO

El transcript de entrevista cubre 5 fases completas (Fase 0, 1, 2, 2.T, 2.U) con 3 informantes distintos (SPONSOR, TECNICO, USUARIO). La cobertura es excepcionalmente rica: 40+ subsecciones respondidas con profundidad y especificidad. Se identifican **5 gaps menores** y **0 gaps críticos o ausentes**. El confidence_score es **0.75**, nivel **PROCEDER CON PRECAUCIÓN**. Todos los gaps son manejables con anotaciones [PENDIENTE] en el SU.md y no impiden la síntesis.

---

## ANÁLISIS POR SECCIÓN DEL SU.MD

### Sección 1 — Contexto organizacional y del problema
**Fuente:** Fase 1.1

**Estado:** Completamente respondida.
- Organización y contexto: distribuidora consumo masivo Colombia, 12 ciudades, Supply Chain ~40 personas.
- Problema concreto: ausencia de pronóstico de demanda por SKU genera quiebres y sobrestock.
- Antecedente: módulo ERP fallido por granularidad insuficiente y falta de participación de usuarios.

**Gaps:** 0

---

### Sección 2 — Impacto y métricas actuales
**Fuente:** Fase 1.2

**Estado:** Completamente respondida.
- Fill rate actual: 87% vs. objetivo 95%. Impacto: COP 800M/punto porcentual.
- Sobrestock: 90 días vs. 45 días estándar. Capital inmovilizado: COP 12.000M.
- Tiempo planeadores: 60% en reactivo. Consecuencias con fecha: 2 contratos canal moderno en riesgo.

**Gaps:** 0

---

### Sección 3 — Solución esperada y alcance
**Fuente:** Fases 1.3, 2.4, 2.U

**Estado:** Sustancialmente respondida. Un gap menor.
- Funcionalidades: dashboard semanal con forecast 4-8 semanas por SKU-bodega, alertas quiebra a 15 días, sugerencia de orden (cantidad + fecha). Tiempo de decisión: medio día/categoría → 30 min/cartera.
- Alcance piloto: 3 bodegas (Bogotá, Medellín, Cali — 70% volumen), 300 SKUs tipo A.
- Límites v1 definidos: 5 elementos fuera de v1, sin OC automáticas en SAP.
- Copiloto, no autopiloto: decisión final siempre del planeador.

**Gap MENOR — G1:**
> **Mecanismo de marcaje de SKUs especiales en v1.** Laura (2.U.2.d) identificó que SKUs con comportamiento atípico (demanda intermitente, pedidos especiales de un cliente, productos en discontinuación) deben poder marcarse como "no pronosticar con el modelo general" desde el inicio del piloto, no después del primer error. El requisito funcional está claro; el mecanismo técnico (quién los marca, dónde, con qué interfaz) no está definido. El synthesizer puede documentar el requisito con anotación [PENDIENTE de diseño técnico por Carlos].
> **Fuente posible:** stakeholder (Carlos — decisión de diseño técnico).

---

### Sección 4 — Stakeholders y gestión del cambio
**Fuente:** Fases 1.4, 2.6

**Estado:** Completamente respondida.
- Mapa de stakeholders: 8 planeadores (4 categorías), Laura Gómez (Coordinadora, límite COP 50M), Gerente de Compras, CFO.
- Proceso de aprobación: planeador → Laura → Gerente de Compras (>COP 50M). CEO solo en cambios de alcance o presupuesto.
- Resistencia: Roberto Sánchez (8 años, influencia de equipo). Requisito: override manual con registro. Plan de escalada en 3 niveles documentado.
- Gestión del cambio: co-diseño con Laura y Roberto antes del kick-off; campeón interno Andrés Torres.
- CEO: alineación pendiente — documentada explícitamente como condición de entrada para comprometer presupuesto, no para iniciar.

**Gaps:** 0 (la alineación pendiente del CEO es estado documentado, no gap del SU.md)

---

### Sección 5 — Datos disponibles y calidad
**Fuente:** Fases 1.5, 2.T

**Estado:** Sustancialmente respondida. Un gap menor.
- Historial confiable real: 28-32 meses promedio por SKU tipo A (no 6 años nominales).
- SKUs tipo A utilizables post-auditoría: 210-230 de 300 (70-77%).
- 5 períodos problemáticos identificados con estrategias de tratamiento explícitas (exclusión, enmascaramiento, reconstrucción activa, decisión diferida).
- Requisitos operativos de Carlos para la auditoría de datos (documento eventos históricos de Laura, acceso a Excel de planeadores, 2 sesiones de validación de 90 y 60 minutos).

**Gap MENOR — G2:**
> **Estructura del Excel de promociones comerciales no verificada.** Carlos (2.T.3.c, supuesto 6) indicó que necesita ver el Excel antes de comprometer que entra en v1 como input. Si la estructura varía por analista o cambia frecuentemente, se pospone a v2 y las temporadas conocidas se modelan como variables calendario. La decisión entre ambas rutas no está tomada. El synthesizer puede documentar ambas ramas con la condición de verificación pre-kick-off.
> **Fuente posible:** documento interno (Excel del área comercial — verificación técnica de Carlos).

---

### Sección 6 — Restricciones técnicas, operativas y presupuestales
**Fuente:** Fases 1.3, 2.5, 2.7, 2.U

**Estado:** Sustancialmente respondida. Un gap menor.
- Plataforma: Azure (activa, aprobada por IT, acuerdos de seguridad firmados).
- Power BI: infraestructura y licencias existentes.
- SAP B1: acceso SQL Server vía servidor de reporting, solo lectura, proceso de credenciales 5-10 días hábiles.
- Presupuesto: rango COP 150-300M total hasta dic-2026 (pendiente aprobación CEO la próxima semana). Plazo fiscal 2026 inamovible. Riesgo reasignación en revisión de julio si no arranca antes de junio.
- 5 puntos de fricción técnica con priorización explícita: override (obligatorio sep-2026), monitoreo pipeline (obligatorio sep-2026), política de fallo SAP (obligatorio sep-2026), Azure ML vs. alternativa (diferible), Azure SQL vs. Blob (diferible).
- Restricciones operativas de Laura (3 no negociables): dato listo antes de 7am del lunes; fallback ante SAP caído con etiqueta de advertencia (nunca pantalla en blanco); override funcional en toda la semana para consultas de jueves.

**Gap MENOR — G3:**
> **Compatibilidad móvil del override no confirmada.** Laura (2.U.2.c) estableció como no negociable que el mecanismo de override debe funcionar desde cualquier dispositivo en el momento (celular, sala de reuniones), no solo desde desktop. Carlos propuso Power Apps embebida en Power BI (2.T.3.b) pero no validó explícitamente su compatibilidad en dispositivos móviles para este caso de uso. Si Power Apps no funciona bien en móvil, la solución técnica del override debe revisarse. El synthesizer puede documentar el requisito como confirmado y marcar la validación de compatibilidad móvil de Power Apps como [PENDIENTE — semana 1 del proyecto].
> **Fuente posible:** stakeholder (Carlos — validación técnica de Power Apps Mobile).

---

### Sección 7 — Criterios de éxito, fracaso y adopción
**Fuente:** Fases 1.3, 2.2, 2.8, 2.U

**Estado:** Completamente respondida. La sección más exhaustivamente cubierta del transcript.
- Métricas cuantitativas: fill rate 91% a 6M, 95% sostenido 2 meses a 12M; días inventario 65/45; MAPE <20% en SKUs tipo A; 80% OC referenciando el forecast.
- Criterios cualitativos: aval explícito de Laura y Roberto (ambos obligatorios para producción).
- Zona gris: ≥89% continúa, 87-89% revisión de causas, <87% fracaso. Autoridad: SPONSOR con input Laura.
- Tasa de intervención: métrica de adopción progresiva (>40% normal en semanas 1-6; >30% en SKUs tipo A a 6M = señal de alerta del modelo).
- Criterios de fracaso inapelable (3): fill rate <87%, datos SAP tan degradados que el modelo supera negativamente al humano, sabotaje activo del equipo de planeación.
- Criterios de abandono de Laura (4): fallos sin explicación en SKUs importantes, tiempo de adopción supera beneficio en 2-3 semanas, dashboard requiere expertise técnica para interpretarse, sistema no respeta excepciones del negocio desde el inicio.

**Gaps:** 0

---

### Sección 8 — Riesgos, dependencias y mitigación
**Fuente:** Fases 2.3, 2.T.3

**Estado:** Sustancialmente respondida. Un gap menor.
- Dependencias IT: credenciales SAP 5-10 días hábiles (iniciar día 1); ventana mantenimiento SAP julio (2 días, no crítico).
- Disponibilidad Laura: auditoría agosto (60% de su tiempo, 2-3 semanas) + feria septiembre (3 días). Piloto inicia última semana agosto.
- 6 supuestos técnicos documentados con 2 críticos: acceso SAP (condición de entrada), capacidad equipo BI (riesgo de transferencia).
- Riesgos de continuidad: Carlos bajo, Laura fuera del período crítico (licencia maternidad feb-2027).

**Gap MENOR — G4:**
> **Sin plan de contingencia ante salida de Roberto Sánchez.** El SPONSOR (2.3.d) identificó explícitamente el riesgo: Roberto tiene conversaciones sobre una posible promoción a coordinador regional antes de octubre. Si ocurre, se pierde al usuario más influyente durante el cierre del piloto. El SPONSOR indicó que "no hay plan de contingencia para ese escenario actualmente". El synthesizer puede documentar el riesgo como identificado y marcar el plan de contingencia como [PENDIENTE — definir antes del kick-off].
> **Fuente posible:** stakeholder (SPONSOR — decisión de gestión de riesgo organizacional).

---

### Sección 9 — Transferencia y sostenibilidad
**Fuente:** Fases 2.8, 2.T.3.c

**Estado:** Sustancialmente respondida. Un gap menor.
- Dueño operativo: Laura Gómez desde enero 2027.
- Capacitación equipo BI: un analista con capacidad de modificar parámetros, reentrenar y diagnosticar (sin rediseñar).
- Transferencia activa durante el desarrollo, no como entregable al final.
- 3 entregables de documentación obligatorios antes del cierre (documentación técnica pipeline, guía de usuario del dashboard, documento de criterios de monitoreo para Laura).
- Criterio de fracaso de transferencia: si en enero 2027 solo Carlos puede mantener el sistema.

**Gap MENOR — G5:**
> **Capacidad real del equipo BI para absorber el mantenimiento no confirmada.** Carlos (2.T.3.c, supuesto 5) señaló que Juan Diego asumió que el equipo de BI absorbe el mantenimiento operativo post-enero 2027, pero Carlos no ha hablado con ese equipo directamente. Si tienen alta carga o no tienen familiaridad con el stack de Azure, la transferencia requiere más tiempo del planificado. Carlos recomendó una conversación explícita con el líder del equipo de BI antes del kick-off para confirmar disponibilidad y alinear expectativas. El synthesizer puede documentar la condición con anotación [PENDIENTE — validar con líder de BI antes del kick-off].
> **Fuente posible:** stakeholder (líder del equipo de BI — no entrevistado).

---

## CONSOLIDACIÓN DE GAPS

| ID | Sección SU.md | Clasificación | Descripción | Fuente posible |
|----|--------------|---------------|-------------|----------------|
| G1 | Solución esperada y alcance | MENOR | Mecanismo técnico de marcaje de SKUs especiales (excepciones del negocio) en v1 — requisito funcional definido, implementación pendiente de diseño | stakeholder (Carlos) |
| G2 | Datos disponibles y calidad | MENOR | Estructura del Excel de promociones comerciales no verificada — determina si entra en v1 o se pospone a v2 | documento interno (Excel comercial) |
| G3 | Restricciones técnicas y operativas | MENOR | Compatibilidad móvil del mecanismo de override (Power Apps) no confirmada — requisito no negociable de Laura | stakeholder (Carlos) |
| G4 | Riesgos y dependencias | MENOR | Sin plan de contingencia ante salida de Roberto Sánchez del equipo de planeación antes de octubre 2026 | stakeholder (SPONSOR) |
| G5 | Transferencia y sostenibilidad | MENOR | Capacidad del equipo BI para absorber mantenimiento post-enero 2027 no confirmada — supuesto no validado | stakeholder (líder BI — no entrevistado) |

**Totales:** 5 MENORES | 0 CRÍTICOS | 0 AUSENTES

---

## CÁLCULO DE CONFIDENCE_SCORE

```
Base:                      1.00
G1 (MENOR):               -0.05
G2 (MENOR):               -0.05
G3 (MENOR):               -0.05
G4 (MENOR):               -0.05
G5 (MENOR):               -0.05
─────────────────────────────────
confidence_score:          0.75
```

**Umbral para complexity=medium:** 0.80
**Nivel resultante:** PROCEDER CON PRECAUCIÓN (0.60 ≤ 0.75 < 0.80)

---

## EVALUACIÓN CUALITATIVA

A pesar del score de 0.75, la entrevista es excepcionalmente completa: 5 fases, 3 informantes distintos, 40+ subsecciones con profundidad y especificidad inusual. Los 5 gaps menores son:

- **Manejables con [PENDIENTE]:** el synthesizer puede redactar las 9 secciones del SU.md con anotaciones explícitas.
- **Resolubles pre-kick-off:** los 5 gaps tienen fuente identificada y ninguno requiere re-entrevistar desde cero.
- **Sin impacto en la estructura central del SU.md:** los gaps afectan detalles de implementación y mitigación, no el problema, el alcance ni los criterios de éxito.

La brecha entre 0.75 y 0.80 refleja 5 incertidumbres reales del proyecto — no deficiencias de la entrevista.

---

## RECOMENDACIÓN

**Proceder a síntesis.** El synthesizer debe incorporar los 5 gaps como anotaciones [PENDIENTE] explícitas con acción de resolución en sus secciones correspondientes del SU.md. Los 5 gaps son resolubles antes del kick-off y no impiden redactar ninguna sección.
