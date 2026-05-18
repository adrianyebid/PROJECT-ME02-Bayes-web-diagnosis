# Presentacion general del proyecto

## 1. Enfoque de la presentacion

La exposicion debe presentar el proyecto como un trabajo integral del equipo, con lenguaje academico y tono estudiantil formal.

Puntos de enfoque:

- problema de diagnostico probabilistico en aplicaciones web distribuidas
- aplicacion de redes bayesianas del Capitulo 13
- implementacion por modulos en Python
- validacion mediante escenarios y analisis de resultados

Duracion sugerida: 8 a 10 minutos.

---

## 2. Estructura sugerida de diapositivas

### Diapositiva 1 - Titulo y contexto

Contenido:

- titulo del proyecto
- curso y capitulo base (Capitulo 13)
- integrantes del equipo
- objetivo general

### Diapositiva 2 - Planteamiento del problema

Contenido:

- dificultad de diagnosticar fallas por sintomas ambiguos
- ejemplos de sintomas compartidos (Error500, LatenciaAlta, ServicioNoDisponible)
- necesidad de inferencia probabilistica

### Diapositiva 3 - Fundamento teorico

Contenido:

- red bayesiana como DAG
- variables aleatorias y dependencia condicional
- tablas CPT
- consulta posterior `P(X | evidencia)`

### Diapositiva 4 - Modelo propuesto

Contenido:

- variables causa y variables sintoma
- relacion causal principal entre nodos
- criterio de modelado: causas -> efectos

### Diapositiva 5 - Arquitectura del sistema

Contenido:

- entrada de evidencia por consola
- motor de inferencia (`enumeration_ask`, `enumerate_all`)
- red bayesiana y CPT
- salida probabilistica e interpretacion

### Diapositiva 6 - Implementacion y menu

Contenido:

- funciones principales del menu
- validacion de entradas (`s`, `n`, `d`)
- control de errores para experiencia de uso robusta

### Diapositiva 7 - Escenarios y resultados

Contenido:

- resumen de los 5 escenarios de prueba
- ejemplo de probabilidad posterior por escenario
- comparacion entre evidencias y cambios de probabilidad

### Diapositiva 8 - Validacion final

Contenido:

- ejecucion desde cero del proyecto
- compilacion correcta de modulos
- estabilidad del sistema ante entradas invalidas
- verificacion de consistencia probabilistica (normalizacion)

### Diapositiva 9 - Rol del Integrante 7

Contenido:

- elaboracion de manual de usuario
- elaboracion de manual tecnico
- preparacion del apoyo de presentacion
- validacion final de operacion y formato

Texto sugerido:

"El rol del Integrante 7 se centró en consolidar la experiencia de uso, la documentacion operativa y la verificacion final de ejecucion del sistema."

### Diapositiva 10 - Conclusiones

Contenido:

- cumplimiento de requisitos del proyecto
- alineacion con el capitulo asignado
- utilidad del modelo para razonamiento bajo incertidumbre
- lineas de mejora futura

---

## 3. Guion academico breve (sin primera persona)

"El proyecto desarrolla un sistema de diagnostico probabilistico de fallas en una aplicacion web distribuida mediante redes bayesianas. El modelo representa causas y sintomas con variables booleanas, y aplica inferencia exacta por enumeracion para calcular probabilidades posteriores. La implementacion se realiza en Python, con estructura modular y validaciones de entrada en consola. La evaluacion se apoya en escenarios representativos, analisis de sensibilidad y comparaciones entre probabilidad a priori y a posteriori. En conjunto, la solucion evidencia la aplicacion directa de los conceptos del Capitulo 13 para resolver un problema real de computacion bajo incertidumbre."

---

## 4. Preguntas probables y respuestas de soporte

Pregunta: "Por que se eligio una interfaz de consola?"

Respuesta: "Porque el foco del proyecto es el motor probabilistico y su explicabilidad; la consola reduce complejidad adicional de interfaz."

Pregunta: "Como se valida que el algoritmo funciona?"

Respuesta: "Mediante ejecucion de escenarios, verificacion de normalizacion, pruebas de entradas invalidas y consistencia de resultados."

Pregunta: "Que aporta la red bayesiana frente a reglas fijas?"

Respuesta: "Permite razonar con incertidumbre y combinar evidencia parcial sin requerir reglas deterministas rigidas."

Pregunta: "Cual fue la contribucion del Integrante 7?"

Respuesta: "Manuales, apoyo de presentacion, robustez del menu de uso y validacion final del funcionamiento integral."

---

## 5. Cierre sugerido

"El proyecto demuestra que el razonamiento probabilistico es una herramienta efectiva para diagnosticar fallas con evidencia incompleta. La integracion de modelo, inferencia y validacion permite una entrega tecnica coherente, reproducible y alineada con el marco teorico del curso."
