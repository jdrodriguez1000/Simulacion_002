Titulo: SU.md Auditoria - su_draft_v1.md
Fecha: 2026-05-14
Auditor: doc_auditor
Version auditada: su_draft_v1.md

---

## Paso A — Verificacion estructural

Las 9 secciones obligatorias estan presentes y desarrolladas:

| N | Seccion | Presente | Desarrollada | Observacion |
|---|---------|----------|--------------|-------------|
| 1 | Encabezado del documento | SI | SI | Stakeholders mapeados, roles y disponibilidad por persona |
| 2 | Contexto y problema de negocio | SI | SI | Organizacion, problema central, antecedentes, impacto cuantificado, consecuencias con fecha |
| 3 | Solucion esperada | SI | SI | Funcionalidades enumeradas (7 items), criterios exito 6 y 12 meses, restricciones no negociables |
| 4 | Stakeholders y estructura de decision | SI | SI | Mapa completo (9 actores), flujo aprobacion, riesgos adopcion con plan escalada, compromisos pendientes |
| 5 | Datos y sistemas | SI | SI | Fuentes, calidad, 5 periodos problematicos, volumen, restricciones de acceso documentadas |
| 6 | Criterios de aceptacion | SI | SI | Periodo de prueba, criterios cuantitativos y cualitativos, zonas grises, criterios de abandono de Laura |
| 7 | Restricciones y dependencias | SI | SI | Fecha limite inamovible, tabla de dependencias criticas, disponibilidad, presupuesto |
| 8 | Arquitectura tecnica y alcance | SI | SI | Alcance piloto, elementos fuera de v1, arquitectura, mecanismo override, supuestos tecnicos |
| 9 | Transferencia y sostenibilidad | SI | SI | Dueno operativo, capacidad requerida, plan transferencia, 3 entregables de documentacion |

Resultado Paso A: ESTRUCTURA COMPLETA. Las 9 secciones estan presentes y desarrolladas con contenido sustantivo. Todos los items PENDIENTE incluyen responsable y condicion de resolucion. Sin secciones vacias ni placeholders sin desarrollar.

---

## Paso B — Contradicciones internas en el draft

### CT-01 — Duracion del piloto inconsistente entre secciones

Clasificacion: contradiccion
Secciones afectadas: Seccion 6, Seccion 7

Evidencia:
- Seccion 6: "Seis semanas de operacion en paralelo... El piloto inicia en la ultima semana de agosto de 2026 y concluye en la primera semana de octubre"
- Seccion 7: "el cierre del presupuesto de compras Q4 ocurre en la primera semana de octubre"

Analisis: Desde la ultima semana de agosto (aprox. 25-31 agosto) hasta la primera semana de octubre son aproximadamente 5 semanas completas, no 6. Con 6 semanas, el cierre del piloto cae en la segunda semana de octubre — despues del cierre del presupuesto Q4 que el propio draft identifica como fecha critica. El numero "seis" es inconsistente con las fechas declaradas en la misma seccion.

---

### CT-02 — Conteo de planeadores adicionales no cierra

Clasificacion: gap_menor
Seccion afectada: Seccion 4

Evidencia:
- Encabezado de fila: "6 planeadores adicionales"
- Desglose en celda: "Alimentos (2), Hogar (2), Personal (1)" = 5

Analisis: El encabezado dice 6, el desglose suma 5. Falta 1 planeador de Bebidas. La seccion 4 lista a Andres Torres como "Planeador de Bebidas" pero no incluye al segundo planeador de esa categoria en el bloque de "planeadores adicionales". Esta omision puede significar que un usuario del equipo quedo fuera del plan de adopcion sin razon documentada.

---

### CT-03 — Ambiguedad entre "piloto" y "produccion" con impacto en la viabilidad del objetivo de diciembre 2026

Clasificacion: gap_critico
Secciones afectadas: Seccion 6, Seccion 7, Seccion 4

Evidencia:
- Seccion 7: "1 de septiembre de 2026 — el modelo debe estar en produccion en esa fecha. Justificacion: los planeadores necesitan minimo 3 meses de uso para impactar el inventario de diciembre."
- Seccion 6: "Seis semanas de operacion en paralelo... piloto inicia ultima semana de agosto, concluye primera semana de octubre."
- Seccion 4: "Pasar a produccion: SPONSOR con aval explicito de Laura." (implica que es decision formal posterior al piloto)

Analisis: El draft usa dos terminos sin definir si son la misma etapa o etapas consecutivas. Interpretacion A: el piloto ES la produccion (empieza agosto, los 3 meses llegan a diciembre — argumento valido). Interpretacion B: la produccion formal ocurre despues del piloto (a mediados de octubre), dejando solo ~2 meses hasta diciembre — insuficientes bajo la premisa de 3 meses declarada. El documento no resuelve esta ambiguedad. Un evaluador sin acceso al transcript no puede determinar si el objetivo de diciembre 2026 es alcanzable con el cronograma propuesto.

---

## Paso C — Contradicciones entre draft y transcript

### CC-01 — Duracion del piloto: transcript dice 5 semanas, draft dice 6

Clasificacion: contradiccion
Seccion del draft: Seccion 6
Referencia transcript: Seccion 2.3.b (SPONSOR)

Texto del transcript:
"iniciar la prueba piloto la ultima semana de agosto, con 5 semanas de prueba en paralelo hasta la primera semana de octubre"

Texto del draft:
"Seis semanas de operacion en paralelo"

Analisis: El SPONSOR fue explicito en el transcript: 5 semanas. El draft introdujo 6 semanas sin justificacion documentada. Las fechas del transcript (ultima semana agosto → primera semana octubre) validan la version de 5 semanas. El cambio a 6 semanas no solo contradice al SPONSOR sino que desplaza el cierre del piloto mas alla de la fecha critica de presupuesto Q4.

---

### CC-02 — Lead time de proveedores (12-18 dias) ausente del draft

Clasificacion: gap_critico
Secciones del draft: Seccion 3, Seccion 5, Seccion 6
Referencia transcript: Seccion 2.U.2.a (Laura Gomez)

Texto del transcript:
"El lead time promedio de nuestros proveedores es de 12 a 18 dias. Si el lunes detecto que un SKU tipo A va a quebrar en 10 dias, ya no tengo margen."

Gap: El draft menciona "sugerencia de fecha de orden considerando el lead time del proveedor" en Secciones 3 y 8, pero en ningun lugar registra el parametro real (12-18 dias). Este dato es el fundamento tecnico de tres decisiones de diseno: (1) por que las alertas son a 15 dias y no a 7 ni a 30, (2) por que se necesita visibilidad de 4-6 semanas, (3) por que el forecast a 4 semanas es el horizonte de validacion. Sin el lead time documentado, estos parametros del sistema parecen arbitrarios para cualquier lector posterior, y el modelo puede ser construido con supuestos incorrectos sobre el lead time real.

---

### CC-03 — Excel de promociones: SPONSOR dice "entra en v1", draft dice "condicional"

Clasificacion: gap_menor
Secciones del draft: Seccion 5, Seccion 8
Referencia transcript: Seccion 2.4.c (SPONSOR) y Seccion 2.T.3.c (Carlos)

Texto del transcript (SPONSOR, 2.4.c):
"El Excel de promociones del area comercial entra como input desde v1 — demasiado importante para SKUs tipo A donde las promociones pueden duplicar la demanda."

Texto del draft (Seccion 5 y 8):
"[PENDIENTE: si estructura del Excel es consistente, carga semanal manual por Carlos; si es inconsistente, se pospone a v2]"

Analisis: La posicion del draft refleja la condicion tecnica identificada por Carlos (Supuesto 6, Fase 2.T), que es metodologicamente correcta. Sin embargo, el draft no documenta la tension entre la declaracion del SPONSOR ("entra en v1") y la condicion tecnica de Carlos (estructura consistente requerida). Si el Excel tiene estructura inconsistente y se pospone a v2, el SPONSOR puede interpretar que no se cumplio lo acordado. Esta tension debe quedar registrada explicitamente como punto de alineacion pendiente SPONSOR-TECNICO.

---

### CC-04 — Criterio de fracaso n.2 de Laura: umbral temporal simplificado

Clasificacion: gap_menor
Seccion del draft: Seccion 6
Referencia transcript: Seccion 2.U.2.d (Laura Gomez)

Texto del transcript:
"El sistema debe mostrar valor visible en las primeras dos o tres semanas del piloto. Si despues de un mes los planeadores sienten que estan haciendo mas trabajo... volvemos al Excel. No en diciembre — en octubre."

Texto del draft (Seccion 6):
"Despues de 2-3 semanas del piloto, el equipo siente que hace mas trabajo del anterior sin mejora perceptible."

Analisis: Laura definio dos umbrales distintos: (1) 2-3 semanas para mostrar valor inicial visible, y (2) un mes como limite final antes de abandonar. El draft colapsa ambos en el primero, generando una expectativa mas rigida que la real. Laura esperaria hasta un mes, no solo 2-3 semanas. Esta diferencia puede crear fricciones innecesarias durante el piloto si el equipo interpreta el draft como que 3 semanas sin valor visible es ya condicion de fracaso.

---

## Paso D — CRA detectados

### CRA-01 — Override mobile-friendly declarado no negociable sobre validacion tecnica pendiente

Clasificacion: cra
Secciones afectadas: Seccion 3 (item 5), Seccion 6 (criterio fracaso n.3 de Laura), Seccion 8

Texto del draft que genera el CRA:
Seccion 3, item 5: "Mecanismo de override: el planeador puede registrar un ajuste al forecast del modelo..." (presentado como funcionalidad comprometida sin condicion)
Seccion 8: "[PENDIENTE: confirmar compatibilidad movil de Power Apps para este caso de uso — requisito no negociable de Laura. Validacion tecnica: Carlos, semana 1 del proyecto]"
Seccion 6, criterio de fracaso n.3 de Laura: "si el dashboard requiere conocimientos estadisticos para interpretarse" — pero tambien del transcript 2.U.2.c: el override desde celular es igualmente no negociable.

Riesgo: La compatibilidad movil de Power Apps para escritura en Azure SQL no esta validada. Si la validacion tecnica de semana 1 falla, un requisito declarado no negociable por Laura no puede cumplirse con la arquitectura propuesta. El draft presenta el override mobile como funcionalidad comprometida en Seccion 3 sin condicionarla a la validacion tecnica de Seccion 8. Cualquier lector de Seccion 3 creyendo que el override mobile es entregable confirmado toma una decision sobre informacion incompleta.

---

### CRA-02 — Arquitectura completa especificada sobre Supuesto 1 (acceso SAP) no validado

Clasificacion: cra
Seccion afectada: Seccion 8

Texto del draft:
"Supuesto critico 1 (condicion de entrada): las tablas de SAP B1 son accesibles con el nivel de detalle necesario para construir la serie de demanda diaria por SKU-bodega. No validado con credenciales reales. Debe verificarse en la semana 1 del proyecto. Sin este supuesto validado, no hay proyecto."

Riesgo: El Supuesto 1 esta correctamente flaggeado, pero la Seccion 8 desarrolla una arquitectura de 5 capas completamente especificada (SAP → Azure Data Lake → Azure ML → Azure SQL → Power BI) como si el supuesto fuera verdadero. Si el acceso a SAP falla o las tablas tienen estructura diferente a la asumida, toda la Seccion 8 requiere rediseno. El draft no condiciona explicitamente el resto de la arquitectura a la validacion del Supuesto 1. Documentos downstream que hereden la Seccion 8 pueden comprometer recursos de desarrollo sobre una base no verificada.

---

### CRA-03 — Criterio de exito cualitativo dependiente de persona con riesgo documentado de salida sin clausula alternativa

Clasificacion: cra
Secciones afectadas: Seccion 6, Seccion 7, Seccion 4

Texto del draft que genera el CRA:
Seccion 6: "Laura Gomez y Roberto Sanchez declaran explicitamente que confian en usar el sistema como punto de partida. Ambos son obligatorios — si el numero de MAPE es bueno pero Roberto no confia, no hay adopcion real."
Seccion 7: "[PENDIENTE: definir plan de contingencia ante salida de Roberto Sanchez antes de octubre 2026; responsable: SPONSOR, antes del kick-off]"

Riesgo: El criterio de aceptacion cualitativa requiere que Roberto declare confianza. Al mismo tiempo, el draft documenta un riesgo conocido de que Roberto salga del equipo antes de octubre. Si Roberto sale, el criterio "ambos son obligatorios" no puede cumplirse como esta escrito — el proyecto formalmente fracasaria por una variable organizacional ajena al desempeno del modelo. El PENDIENTE del plan de contingencia no resuelve el CRA: el criterio de exito mismo necesita una clausula alternativa que defina que reemplaza la declaracion de Roberto si ya no esta en el equipo.

---

### CRA-04 — Plan de transferencia a equipo BI comprometido sin validar capacidad directamente

Clasificacion: cra
Seccion afectada: Seccion 9, Seccion 8 (Supuesto 2)

Texto del draft:
Seccion 9: "El equipo de BI debe absorber el mantenimiento operativo del pipeline... [PENDIENTE: validar con el lider del equipo de BI su disponibilidad y familiaridad con el stack de Azure... antes del kick-off]"
Seccion 8, Supuesto 2: "Juan Diego asumio que si, pero Carlos no ha hablado con ese equipo directamente."

Riesgo: La Seccion 9 describe un plan de transferencia activa durante el desarrollo (no al final) que presupone disponibilidad y conocimiento del stack por parte del equipo BI. Este plan es una promesa operativa que puede ser materialmente falsa. Si el equipo BI no tiene capacidad o familiaridad con Azure Data Factory y el stack propuesto, el criterio de fracaso de transferencia declarado en el mismo documento ("si en enero 2027 el sistema solo puede ser mantenido por Carlos, el proyecto no termino bien") se vuelve resultado inevitable desde el dia 1. El plan de transferencia esta escrito en tiempo presente como si fuera una decision acordada cuando en realidad es una hipotesis no verificada con el actor clave.

---

## Resumen

gaps_criticos=2, gaps_menores=4, contradicciones=2, cra=4

| ID | Tipo | Descripcion breve | Secciones |
|----|------|-------------------|-----------|
| CT-03 | gap_critico | Ambiguedad piloto vs. produccion — viabilidad del objetivo de diciembre 2026 | S6, S7, S4 |
| CC-02 | gap_critico | Lead time de proveedores (12-18 dias) ausente — fundamento de alertas y sugerencia de orden | S3, S5, S6 |
| CT-02 | gap_menor | Conteo planeadores: "6" declarado vs 5 en desglose; falta 1 planeador de Bebidas | S4 |
| CC-03 | gap_menor | Excel promociones: tension SPONSOR ("v1") vs condicion tecnica Carlos no documentada | S5, S8 |
| CC-04 | gap_menor | Criterio fracaso n.2 Laura: draft simplifica a 2-3 semanas; transcript tiene doble umbral (2-3 sem + 1 mes) | S6 |
| GM-03 | gap_menor | Narrativa CEO para separar desempeno del modelo de fill rate global no capturada en el draft | S6 |
| CT-01/CC-01 | contradiccion | Duracion del piloto: 6 semanas (draft) vs 5 semanas (transcript 2.3.b SPONSOR) | S6 |
| CC-03 | contradiccion | Excel promociones: declaracion SPONSOR ("entra en v1") vs posicion draft (condicional segun estructura) | S5, S8 |
| CRA-01 | cra | Override mobile-friendly declarado no negociable pero validacion tecnica pendiente (Power Apps) | S3, S6, S8 |
| CRA-02 | cra | Arquitectura completa especificada sobre Supuesto 1 (acceso SAP) no validado | S8 |
| CRA-03 | cra | Criterio exito cualitativo (Roberto obligatorio) dependiente de persona con riesgo documentado de salida | S6, S7 |
| CRA-04 | cra | Plan de transferencia BI comprometido sin validar capacidad directamente con ese equipo | S9, S8 |

---

## Recomendaciones para su_evaluator

1. [CT-03 — gap_critico] Verificar si el draft define explicitamente que el piloto ES la produccion (no una etapa previa). Si la ambiguedad no se resuelve, el argumento de viabilidad del objetivo de diciembre 2026 no puede evaluarse. Solicitar aclaracion al su_synthesizer en v2 antes de aprobar el SU.md.

2. [CC-02 — gap_critico] El parametro de lead time (12-18 dias) debe estar documentado en Seccion 5 o Seccion 8. Sin este dato, la alerta de quiebre a 15 dias y la sugerencia de fecha de orden no tienen base numerica verificable. Bloquear aprobacion hasta que se incorpore.

3. [CRA-03 — cra] El criterio de exito cualitativo "Laura Y Roberto, ambos obligatorios" debe examinarse en combinacion con el PENDIENTE de plan de contingencia por salida de Roberto. Si el draft no define criterio alternativo valido para el caso de salida de Roberto, el proyecto tiene una condicion de fracaso estructural no relacionada con el desempeno del modelo. Solicitar clausula alternativa explicita en v2.

4. [CRA-01 — cra] La funcionalidad de override mobile se presenta en Seccion 3 como entregable comprometido y en Seccion 8 como pendiente de validacion. Esta inconsistencia interna debe resolverse: o el override mobile es condicional en Seccion 3, o la validacion tecnica de Seccion 8 debe completarse antes de aprobar el SU.md.

5. [CT-01/CC-01 — contradiccion] La duracion del piloto debe corregirse a 5 semanas (valor explicito del transcript) o justificarse el cambio a 6 semanas con nueva confirmacion del SPONSOR. Las fechas declaradas (ultima semana agosto a primera semana octubre) respaldan 5 semanas. Este cambio tiene impacto directo en la relacion con la fecha de cierre de presupuesto Q4.

6. [CRA-04 — cra] El plan de transferencia del equipo BI debe marcarse explicitamente como hipotesis pendiente de validacion, no como plan acordado. Si se aprueba el SU.md con este lenguaje como si fuera decision tomada, los documentos downstream de arquitectura y sostenibilidad heredaran un supuesto falso con consecuencias operativas en enero 2027.
