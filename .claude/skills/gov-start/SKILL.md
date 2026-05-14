---
name: gov-start
description: Punto de entrada del harness de gobernanza. Verifica estado, ejecuta gov_init.py y lanza el doc_orchestrator. Usar al iniciar o retomar una sesión de gobernanza.
allowed-tools: [Bash, Read]
---

# Skill: /gov-start

Punto de entrada del harness de gobernanza. Ejecuta 6 pasos en secuencia para iniciar o retomar el harness de forma segura.

---

## Paso 0 — Detectar primera ejecución y crear archivos de estado iniciales

Antes de verificar la estructura de carpetas, comprobar la existencia de los dos archivos de estado JSON:

- `project_state.json` (raíz del proyecto)
- `governance/gov_state.json`

Aplicar la siguiente lógica:

**Caso A — Ninguno de los dos existe (primera ejecución legítima):**

1. Si `governance/` no existe, crearla.
2. Crear `project_state.json` en la raíz con el contenido:
   ```json
   {"active_harness": "governance", "product": {"status": "locked"}}
   ```
3. Crear `governance/gov_state.json` con el contenido:
   ```json
   {"su": {"status": "in_progress", "phase": "interview_phase1"}}
   ```
4. Informar al usuario: `[Paso 0] Primera ejecución detectada. Archivos de estado creados. Continuando al Paso 1.`
5. Continuar al Paso 1.

**Caso B — Solo uno de los dos existe (estado parcialmente corrupto):**

No crear ningún archivo. Mostrar al usuario:

```
[Paso 0] ADVERTENCIA — Estado parcialmente corrupto detectado.

Solo uno de los dos archivos de estado JSON existe:
- project_state.json: {existe / no existe}
- governance/gov_state.json: {existe / no existe}

Este estado indica una ejecución interrumpida o corrupción parcial.
gov_init.py reportará status: critical en el Paso 2.
Revisar manualmente ambos archivos antes de continuar.
```

Continuar al Paso 1 (gov_init.py detectará el faltante y reportará critical).

**Caso C — Ambos existen:**

No hacer nada. Continuar directamente al Paso 1.

---

## Paso 1 — Verificar estructura de carpetas y remoto GitHub

Confirmar que los directorios y archivos críticos existen:

- `governance/` existe
- `governance/su/` existe
- `scripts/gov_init.py` existe
- `.claude/agents/doc_orchestrator.md` existe
- `project_state.json` existe

Si alguno falta, reportar exactamente qué falta y detener. No continuar al Paso 2 si la estructura está incompleta.

**Verificación de remoto GitHub (recomendado, no bloqueante):**

Ejecutar:
```bash
git remote get-url origin
```

- Si retorna una URL con `github.com` → continuar silenciosamente.
- Si no hay remoto o la URL no es de GitHub → mostrar al usuario:

```
[Paso 1] AVISO — No se detectó un remoto GitHub configurado.

El harness hace commits git en hitos clave y los empuja a GitHub para respaldo
externo y trazabilidad. Sin remoto, los artefactos quedan solo en local y
gov_init.py reportará status: "warning".

Para configurar el remoto antes de continuar:
  git remote add origin https://github.com/<usuario>/<repositorio>.git
  git push -u origin <rama>

El harness puede continuar en modo local. Ejecutar /gov-start nuevamente
después de configurar el remoto para habilitar los pushes automáticos.
```

Continuar al Paso 2 independientemente del resultado (degradación elegante).

---

## Paso 2 — Ejecutar gov_init.py

Ejecutar el script de verificación de integridad:

```bash
python scripts/gov_init.py
```

El script verifica:
- `gov_state.json` y `project_state.json` son JSON válido
- La fase declarada en `gov_state.json` es consistente con los archivos en disco
- Git está disponible y funcional
- `governance/su/su_sprint_contract.md` existe si la fase lo requiere

El script escribe el resultado en `governance/gov_init_report.json` y retorna:
- Exit code 0 → `status: "ok"`
- Exit code 1 → `status: "warning"` (inconsistencia recuperable)
- Exit code 2 → `status: "critical"` (JSON corrupto o inconsistencia irrecuperable)

---

## Paso 3 — Leer gov_init_report.json

Leer `governance/gov_init_report.json` y determinar el `status`.

---

## Paso 4a — Si status es "ok" o "warning"

Lanzar el agente `doc_orchestrator` con el siguiente prompt:

```
Actúa como doc_orchestrator. 

gov_init.py acaba de ejecutarse. gov_init_report.json tiene status="{status}".

{Si status="warning": El orquestador debe leer gov_init_report.json, identificar la inconsistencia reportada, auto-repararla y registrar la reparación en gov_history.log antes de continuar.}

Sigue el protocolo de inicio de sesión completo:
1. Lee gov_init_report.json (ya ejecutado — usa el status={status})
2. Lee project_state.json
3. Lee governance/gov_state.json
4. Lee governance/gov_progress.txt
5. Lee governance/gov_history.log (últimas 20 líneas)
6. Ejecuta git log --oneline -10
7. Guarda tu plan en gov_progress.txt
8. Registra el inicio de sesión en gov_history.log
9. Continúa el harness desde la fase registrada en gov_state.json
```

---

## Paso 4b — Si status es "critical"

No lanzar el `doc_orchestrator`. Mostrar al usuario:

```
HARNESS DETENIDO — gov_init.py reportó status: critical

Inconsistencias detectadas:
{listar gov_init_report.json.inconsistencies}

Acción recomendada: {gov_init_report.json.recommended_action}

El harness no puede continuar con estado corrupto. Reparar manualmente 
los archivos indicados y volver a ejecutar /gov-start.
```

---

## Paso 5 — El doc_orchestrator retoma

Una vez lanzado, el `doc_orchestrator` opera de forma autónoma:
- Lee los archivos de estado en el orden obligatorio
- Identifica el documento activo y la fase exacta
- Retoma desde el checkpoint registrado sin repetir pasos completados
- Informa al usuario qué va a hacer antes de invocar subagentes
