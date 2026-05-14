# CLAUDE.md: Protocolos IA/DS (SpecDD + TDD)

## PRINCIPIOS DE INGENIERÍA

**PI-1. Razona antes de actuar.** Debes exponer pros, contras y suposiciones. Ante ambigüedad, detente y consulta; nunca elijas en silencio.

**PI-2. Simplicidad primero.** Código mínimo con interfaces simples. Sin abstracciones, parámetros ni configurabilidad no solicitados.

**PI-3. Cambios quirúrgicos.** Solo toca lo necesario para la tarea. No refactorices lo que funciona. No borres código muerto preexistente sin autorización.

**PI-4. Slices verticales.** Una funcionalidad completa (datos→interfaz) a la vez. Valida integración con un "Tracer Bullet" antes de ampliar.

**PI-5. Orientado a comportamiento.** Toda tarea tiene un test que la respalda. Definición de Terminado = test en verde. Sin excepción.

## REGLAS DEL HARNESS

- **Persistencia total:** Todo lo producido, decidido o asumido se registra en un archivo; nunca en memoria.
- **Adherencia a plantillas:** Respeta la estructura de artefactos sin agregar, omitir ni expandir secciones.
- **Una sola tarea:** No avances hasta que el objetivo actual esté completado y aprobado.
- **Separación de roles:** Quien implementa no evalúa; quien revisa no reescribe.
- **Cero decisiones silenciosas:** Ante ambigüedad, detente y consulta; documenta toda decisión de diseño.
- **Revisión independiente:** Revisiones por agente o instancia separada; no autoevaluación.
- **Doble validación:** Aprobación del stakeholder (negocio) + revisión técnica independiente. Ambas obligatorias.
