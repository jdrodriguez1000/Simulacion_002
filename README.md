# Harness de Gobernanza — SU.md

Guía de operación para el harness de gobernanza. Un humano sin contexto previo puede iniciar o retomar el harness leyendo este documento.

---

## Sección 1 — Propósito y contexto

Este repositorio contiene el **harness de gobernanza IA/DS**, un sistema de agentes que produce documentos de gobernanza de proyectos de manera estructurada, verificable y recuperable ante fallos.

El primer documento que produce el harness es el **SU.md** (Shared Understanding Document): el contrato de entendimiento entre el cliente y el equipo sobre el problema de negocio. Todos los documentos posteriores (BRD, BDD, SAD, SpecDD, Feasibility, Backlog) dependen de él.

**Regla fundamental:** Un SU.md ambiguo contamina en cascada todos los documentos que dependen de él. Su aprobación es el prerrequisito más crítico del harness.

**Advertencia:** El harness de producto (`product/`) permanece bloqueado (`product.status: "locked"`) hasta que la gobernanza esté completa. No se debe iniciar trabajo de producto antes de que `gov_state.json` refleje `governance.status: "completed"`.

---

## Sección 2 — Estructura de carpetas

```
raíz/
├── README.md                          ← este archivo
├── CLAUDE.md                          ← principios de ingeniería y reglas del harness
├── project_state.json                 ← harness activo y estado del producto
├── gov_metrics_catalog.json           ← catálogo de métricas para el harness_director
│
├── .claude/
│   ├── agents/
│   │   ├── doc_orchestrator.md        ← orquestador principal (no invocar directamente)
│   │   ├── doc_auditor.md             ← auditor de documentos (detecta gaps y contradicciones)
│   │   ├── harness_director.md        ← mide eficiencia del harness (independiente)
│   │   ├── su_interviewer.md          ← conduce entrevista Fase 1 y Fase 2 para SU.md
│   │   ├── su_synthesizer.md          ← genera borrador del SU.md desde el transcript
│   │   ├── su_evaluator.md            ← evalúa el borrador con rúbrica calibrada
│   │   ├── su_needs_analyzer.md       ← clasifica gaps y calcula confidence_score
│   │   └── post_mortem_agent.md       ← analiza fallos del circuit breaker
│   └── skills/
│       └── gov-start/
│           └── SKILL.md               ← skill /gov-start (punto de entrada recomendado)
│
├── governance/
│   ├── gov_state.json                 ← estado actual: documento activo, fase, complejidad
│   ├── gov_progress.txt               ← orientación narrativa del progreso
│   ├── gov_history.log                ← log cronológico de acciones de agentes
│   ├── gov_init_report.json           ← resultado del último gov_init.py
│   ├── gov_failure_modes.json         ← registro acumulativo de fallos entre runs
│   └── su/
│       ├── su_sprint_contract.md      ← definición de "SU.md terminado"
│       ├── su_interview.md            ← transcript completo Fase 1 + Fase 2
│       ├── su_knowledge_gaps.md       ← gaps detectados antes de sintetizar
│       ├── su_draft_v{n}.md           ← borradores iterativos
│       ├── su_review.md               ← scores del evaluador + gaps del auditor
│       ├── su_approved.md             ← versión final aprobada (inmutable)
│       ├── su_metrics.json            ← métricas del ciclo SU.md
│       └── gov_postmortem_su_{fecha}.md ← post-mortem si se activó circuit breaker
│
├── scripts/
│   └── gov_init.py                    ← verificación de integridad antes de cada sesión
│
└── project/                           ← harness de producto (bloqueado hasta gobernanza)
```

---

## Sección 3 — Cómo iniciar el harness

### Prerequisito recomendado: repositorio remoto en GitHub

El harness hace commits git en cada hito clave y los empuja a GitHub para respaldo externo y visibilidad del equipo. Sin remoto, el harness opera en modo local (degradación elegante) pero los artefactos no tendrán respaldo externo y `gov_init_report.json` reportará `status: "warning"`.

Para configurar el remoto antes de ejecutar `/gov-start`:

```bash
git remote add origin https://github.com/<usuario>/<repositorio>.git
git push -u origin <rama>
```

Si el remoto ya está configurado, no es necesario hacer nada — el harness lo detecta automáticamente.

### Primera vez (harness no iniciado)

1. Verificar que `project_state.json` existe con `active_harness: "governance"`.
2. Ejecutar el skill `/gov-start` desde Claude Code.
3. El skill verifica la estructura, ejecuta `scripts/gov_init.py` y lanza el `doc_orchestrator`.
4. El `doc_orchestrator` creará `governance/su/su_sprint_contract.md` si no existe y comenzará la entrevista con el stakeholder.

### Retomar una sesión interrumpida

1. Ejecutar `/gov-start` — el skill detecta automáticamente el estado actual.
2. El `gov_init.py` verificará la consistencia entre `gov_state.json` y los archivos en disco.
3. El `doc_orchestrator` leerá `gov_state.json` para saber en qué fase estaba y retomará desde ese punto sin repetir pasos completados.

### Sin el skill (inicio manual)

```bash
python scripts/gov_init.py
```

Luego lanzar el agente `doc_orchestrator` desde Claude Code con el comando:

```
Actúa como doc_orchestrator. Lee gov_init_report.json primero.
```

### Señales de que el harness necesita intervención humana

- `gov_state.json` tiene `phase: "human_intervention_required"` → el circuit breaker se activó; revisar `governance/su/gov_postmortem_su_{fecha}.md`
- `gov_init_report.json` tiene `status: "critical"` → JSON corrupto; reparar manualmente y re-ejecutar `gov_init.py`
- `gov_history.log` tiene entrada `"SU escalado a humano tras 3 iteraciones"` → revisar `su_review.md` para entender por qué no convergió

---

## Sección 4 — Agentes disponibles y roles

| Agente | Invocado por | Cuándo |
|--------|-------------|--------|
| `doc_orchestrator` | `/gov-start` (skill) o manualmente | Al iniciar o retomar cualquier sesión del harness |
| `su_interviewer` | `doc_orchestrator` | Para conducir Fase 1 y Fase 2 de entrevista con el stakeholder |
| `su_needs_analyzer` | `doc_orchestrator` | Después de Fase 2 completa, antes de invocar al synthesizer |
| `su_synthesizer` | `doc_orchestrator` | Cuando la entrevista supera el umbral de confidence |
| `su_evaluator` | `doc_orchestrator` | En paralelo con `doc_auditor`, tras generar cada draft |
| `doc_auditor` | `doc_orchestrator` | En paralelo con `su_evaluator`, para detectar gaps y contradicciones |
| `post_mortem_agent` | `doc_orchestrator` | Solo cuando se activa el circuit breaker (3 iteraciones sin aprobar) |
| `harness_director` | `doc_orchestrator` | Después de aprobar `su_approved.md`, para calcular métricas del ciclo |

**Regla de invocación:** Solo el `doc_orchestrator` invoca subagentes. Nunca invocar un subagente directamente salvo para diagnóstico.

**Agentes vs. skills:**
- **Agentes** (`.claude/agents/`): instancias de Claude con instrucciones específicas; el `doc_orchestrator` los lanza con la herramienta `Agent`.
- **Skills** (`.claude/skills/`): comandos slash (`/gov-start`) disponibles en Claude Code; ejecutan secuencias de pasos predefinidos en el contexto de la conversación actual.

---

## Sección 5 — Archivos de estado: orden de lectura obligatorio

Al inicio de **cada sesión**, el `doc_orchestrator` lee los archivos en este orden exacto:

| Orden | Archivo | Propósito |
|-------|---------|-----------|
| 1 | `governance/gov_init_report.json` | Determinar si el ambiente es íntegro antes de cualquier decisión |
| 2 | `project_state.json` | Saber qué harness está activo y si el producto está bloqueado |
| 3 | `governance/gov_state.json` | Saber qué documento está en progreso y en qué fase exacta |
| 4 | `governance/gov_progress.txt` | Orientación narrativa del progreso (qué se hizo, qué sigue) |
| 5 | `governance/gov_history.log` | Últimas decisiones tomadas y timestamps de agentes |

Este orden es obligatorio. Leer `gov_state.json` antes de `gov_init_report.json` puede llevar a tomar decisiones sobre un estado inconsistente.

---

## Sección 6 — Reglas de operación críticas

**Estado:**
- Solo el `doc_orchestrator` escribe en `gov_state.json`, `gov_progress.txt` y `gov_history.log`.
- Ningún subagente modifica archivos de estado directamente; solo escribe sus artefactos de output.
- Toda decisión de diseño se documenta en `gov_history.log` antes de ejecutar la acción.

**Commits git:**
- Cada fase completada requiere un commit con mensaje descriptivo.
- Mensajes obligatorios: `"SU Phase1 interview completed"`, `"SU Phase2 interview completed"`, `"SU knowledge gaps analyzed"`, `"SU Draft v{n} generated"`, `"SU APPROVED by stakeholder"`.
- Nunca omitir commits — son la única fuente de verdad temporal para el `harness_director`.

**Contextos frescos:**
- Cada subagente corre en un contexto fresco (herramienta `Agent`).
- Los subagentes leen sus inputs del filesystem, no del historial de conversación del orquestador.
- Esto previene la "context anxiety": degradación del razonamiento por acumulación de tokens.

**Aprobaciones:**
- Ningún documento se aprueba automáticamente sin presentarlo al stakeholder.
- La aprobación humana se registra en `gov_history.log` antes de copiar a `su_approved.md`.
- `su_approved.md` es inmutable: no se modifica después de creado.

**Circuit breaker:**
- Máximo 3 iteraciones `su_synthesizer → su_evaluator` por documento.
- A la tercera iteración sin aprobar: `post_mortem_agent` analiza la causa raíz, `gov_state.json` pasa a `phase: "human_intervention_required"`, el harness se detiene.

---

## Sección 7 — Skill `/gov-start`

El skill `/gov-start` es el **punto de entrada recomendado** para iniciar o retomar el harness. Ejecuta 6 pasos en secuencia:

| Paso | Acción | Qué verifica |
|------|--------|-------------|
| 0 | Detectar primera ejecución | Si ambos JSON de estado faltan → los crea. Si solo uno falta → advierte. Si ambos existen → continúa. |
| 1 | Verificar estructura de carpetas | `governance/`, `governance/su/`, `scripts/`, `.claude/agents/` existen |
| 2 | Ejecutar `scripts/gov_init.py` | Integridad de JSON, consistencia fase↔filesystem, disponibilidad de git |
| 3 | Leer `governance/gov_init_report.json` | Resultado: `ok`, `warning` o `critical` |
| 4a | Si `status: ok` o `warning` | Lanzar `doc_orchestrator` con contexto del init report |
| 4b | Si `status: critical` | Mostrar errores, indicar acción de reparación manual, detener |
| 5 | El `doc_orchestrator` retoma | Lee archivos de estado en orden obligatorio y continúa el harness |

**Para usar el skill:** Escribir `/gov-start` en el chat de Claude Code.

**Distinción agentes vs. skills:**
- Los **agentes** (`.claude/agents/*.md`) son prompts que definen la identidad y comportamiento de una instancia de Claude; el `doc_orchestrator` los lanza como subagentes en contextos frescos usando la herramienta `Agent`.
- Los **skills** (`.claude/skills/*/SKILL.md`) son secuencias de instrucciones que Claude ejecuta en el contexto de la conversación actual cuando el usuario escribe el comando slash correspondiente (`/gov-start`). No crean subagentes — operan directamente.

---

## Sección 8 — Glosario

| Término | Definición |
|---------|-----------|
| **SU.md** | Shared Understanding Document. Primer documento de gobernanza. Captura el entendimiento compartido del problema de negocio entre cliente y equipo. Prerrequisito para todos los documentos posteriores. |
| **Circuit breaker** | Mecanismo de seguridad que detiene el harness tras 3 iteraciones sin aprobar un documento. Activa el `post_mortem_agent` y escala al humano. |
| **Context anxiety** | Degradación del razonamiento del modelo cuando el contexto acumula demasiados tokens. El harness lo previene ejecutando cada subagente en contexto fresco con inputs del filesystem. |
| **Checkpoint** | Marca de estado `[COMPLETADO timestamp]` en `su_interview.md` que permite al `su_interviewer` relanzado retomar desde la primera sección `[PENDIENTE]` sin repetir trabajo. |
| **Sprint contract** | `su_sprint_contract.md`: define qué significa "SU.md terminado" antes de iniciar el sprint. Incluye criterios de entrada, exit criteria, límite de iteraciones y criterios de rechazo automático. |
| **Extended Thinking** | Modo de razonamiento extendido de Claude. El harness usa dos variantes según el agente: *visible thinking* (planificación previa completa, `su_synthesizer` v1 complejidad ALTA) e *interleaved thinking* (razonamiento post-lectura por sección, `su_evaluator` y `doc_auditor` complejidad ALTA). |
| **confidence_score** | Métrica calculada por `su_needs_analyzer` (0.0–1.0) que indica qué tan lista está la entrevista para producir un draft aprobable. Fórmula: `1.0 - (críticos×0.20) - (menores×0.05) - (ausentes×0.03)`. El orquestador solo avanza al synthesizer cuando supera el umbral de su nivel de complejidad. |
| **gov_failure_modes.json** | Registro acumulativo entre runs de los fallos del harness. Escrito por `post_mortem_agent`. El `doc_orchestrator` lo lee al inicio de cada run para incluir patrones conocidos como advertencia al agente responsable. |
