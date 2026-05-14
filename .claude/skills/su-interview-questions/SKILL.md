---
name: su-interview-questions
description: Preguntas literales de todas las fases de entrevista del SU.md. Carga Fase 0 (3 preguntas de mapeo), Fase 1 (5 secciones, ~20 preguntas), Fase 2 (8 secciones, ~30 preguntas), Fase 2.T (3 secciones, ~12 preguntas técnicas) y Fase 2.U (2 secciones, ~8 preguntas de usuario). Invocada por su_interviewer al inicio de cada fase.
user-invocable: false
---

# Skill: /su-interview-questions

Preguntas literales de todas las fases de entrevista del SU.md, organizadas por fase y sección. Invocada por `su_interviewer` al inicio de cada fase para cargar las preguntas antes de comenzar.

---

## FASE 0 — Preguntas de mapeo de stakeholders

1. "Para arrancar bien el proyecto, necesito identificar a las personas clave. Además de usted, ¿hay alguien en la empresa que sea el experto técnico en los sistemas o datos que usará este proyecto? ¿Nombre y cargo?"
2. "¿Hay usuarios finales que usarán el sistema día a día y que podrían darnos su perspectiva operativa? ¿Nombre y cargo?"
3. "¿Estarían disponibles para una conversación breve si la necesitamos?"

---

## FASE 1 — Preguntas abiertas (Exploración del problema)

### 1.1 El problema central

- ¿Cuál es el problema principal que quieres resolver con este proyecto?
- ¿Qué está pasando hoy en tu negocio que no debería estar pasando?
- ¿Qué oportunidad de negocio quieres aprovechar?
- ¿Cuándo empezó este problema o cuándo se volvió relevante resolverlo?

### 1.2 El impacto en el negocio

- ¿Cómo afecta este problema a tu empresa hoy?
- ¿Quiénes dentro de tu organización se ven perjudicados por este problema?
- ¿Qué consecuencias tiene para tus clientes?

### 1.3 Intentos previos

- ¿Qué has intentado antes para resolver este problema?
- ¿Por qué no funcionó o fue insuficiente?

### 1.4 La visión del éxito

- ¿Cómo se vería el éxito para ti cuando este proyecto esté terminado?
- ¿Qué debería poder hacer tu equipo o tu empresa que hoy no puede hacer?
- ¿Qué dejaría de ocurrir que hoy ocurre y te genera problemas?

### 1.5 Contexto organizacional

- ¿Hay algo importante sobre tu empresa o tu industria que debamos entender para resolver bien este problema?
- ¿Hay otras iniciativas en tu empresa relacionadas con este problema?

---

## FASE 2 — Preguntas específicas (Confirmación y cierre)

### 2.1 Contexto del negocio

- ¿En qué industria opera tu empresa? (ej: retail, salud, finanzas, manufactura)
- ¿Cuántos clientes, empleados o transacciones involucra el área afectada por el problema?
- ¿Hace cuánto tiempo existe este problema (meses, años)?
- ¿Hay regulaciones legales o de cumplimiento que afecten este proyecto? ¿Cuáles?

### 2.2 Impacto cuantificable

- ¿Cuánto dinero estimas que pierde la empresa por este problema cada mes?
- ¿Cuántas horas de trabajo se pierden por semana por este problema?
- ¿Cuántas personas están afectadas directamente?
- ¿Tiene algún efecto en la satisfacción o retención de clientes? ¿Puedes estimarlo?

### 2.3 Criterios de éxito del proyecto

- ¿Qué número o indicador específico debe mejorar para que consideres que el proyecto fue exitoso?
- ¿En cuánto tiempo esperas ver ese resultado (semanas, meses)?
- ¿Quién en tu organización decide si el proyecto fue exitoso o no?
- Si tuvieras que elegir una sola métrica de negocio para medir el éxito, ¿cuál sería?

### 2.4 Stakeholders y responsabilidades

- ¿Quién toma la decisión final de aprobación del proyecto?
- ¿Quién usará los resultados del sistema día a día? ¿Qué cargo tiene?
- ¿Cuántas personas en total usarán el sistema día a día? ¿Cuántos por cada rol?
- ¿Hay áreas o personas dentro de la empresa que podrían oponerse o resistirse al proyecto?
- ¿Quién tiene acceso a los datos o información que necesitamos?

### 2.5 Alcance: dentro y fuera

- ¿Qué partes del proceso o del negocio SÍ deben estar cubiertas por este proyecto?
- ¿Hay partes del negocio que explícitamente NO deben ser tocadas o cambiadas?
- ¿Hay sistemas o herramientas que ya existen y que el proyecto debe respetar o integrarse con ellos?

### 2.6 Datos disponibles (visión del cliente)

- ¿Tienes datos históricos sobre el problema? ¿De cuántos años aproximadamente?
- ¿Dónde están guardados esos datos hoy? (ej: Excel, sistema interno, base de datos, papel)
- ¿Esos datos son de acceso libre o hay restricciones para usarlos?
- ¿Hay datos que sabes que necesitaríamos pero que hoy no existen o no están disponibles?
- ¿Hay períodos donde los datos podrían estar incompletos o tener menor calidad? Por ejemplo, ¿algún mes o año donde los registros no estén completos?
- ¿Ha habido cambios de sistema o migraciones de datos en los últimos años que puedan haber afectado el histórico?

### 2.7 Restricciones del proyecto

- ¿Hay una fecha límite para tener los primeros resultados? ¿Por qué esa fecha?
- ¿Hay un presupuesto definido para el proyecto?
- ¿Hay tecnologías, plataformas o proveedores que la empresa ya usa y que debemos usar o no podemos usar?
- ¿Hay restricciones de confidencialidad o seguridad sobre la información del proyecto?
- ¿Hay restricciones sobre cómo los usuarios accederán al sistema? Por ejemplo: ¿operan desde escritorio, tablet o dispositivo móvil? ¿Tienen conexión a internet estable o trabajan en zonas con conectividad limitada?

### 2.8 Riesgos conocidos

- ¿Qué es lo que más te preocupa que podría salir mal en este proyecto?
- ¿Ha habido proyectos similares en tu empresa o industria que hayan fallado? ¿Por qué fallaron?
- ¿Hay cambios próximos en tu empresa (reorganizaciones, fusiones, cambios regulatorios) que puedan afectar este proyecto?

---

## FASE 2.T — Preguntas de mini-entrevista técnica

### 2.T.1 — Estructura y volumen de datos

- ¿En qué formato están los datos? (archivo de texto, base de datos, API, servicio externo, otro)
- ¿Cuántos registros o transacciones aproximados tiene el histórico?
- ¿Los datos están en un solo sistema o distribuidos en varios?
- ¿Quién es el propietario o administrador de esos datos?

### 2.T.2 — Calidad y completitud

- ¿Hay períodos donde los datos podrían estar incompletos o con menor calidad?
- ¿Ha habido cambios de sistema o migración de datos en los últimos años que afecten la continuidad histórica?
- ¿Hay campos vacíos o registros corruptos que conozcas?

### 2.T.3 — Acceso y restricciones técnicas

- ¿Cómo se accede a los datos hoy? ¿Hay credenciales, VPN o permisos especiales requeridos?
- ¿Qué sistemas existentes debe respetar o integrarse el nuevo sistema?
- ¿Hay restricciones de conectividad (zonas sin internet, redes cerradas)?
- ¿En qué tipo de dispositivos o infraestructura se desplegará el sistema?

---

## FASE 2.U — Preguntas de mini-entrevista de usuario final

### 2.U.1 — Contexto de uso diario

- ¿Cómo es su flujo de trabajo típico hoy, paso a paso, en el área que este proyecto busca mejorar?
- ¿Desde qué dispositivo trabajará con el nuevo sistema? (computadora de escritorio, tablet, celular, dispositivo especial)
- ¿Trabaja en una ubicación fija con conexión estable o en diferentes lugares con conectividad variable?
- ¿Cuántas veces al día interactuaría con el sistema?

### 2.U.2 — Pain points y expectativas

- ¿Qué parte del proceso actual le genera más fricción o pérdida de tiempo?
- ¿Qué pasos del flujo actual cambiarían con el nuevo sistema?
- ¿Hay restricciones de tiempo o de contexto (ej: hay que registrar datos en el momento, sin poder esperar)?
- ¿Qué haría que el sistema no le sirva en su día a día?
