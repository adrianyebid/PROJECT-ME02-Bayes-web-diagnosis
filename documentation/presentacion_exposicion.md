# Presentacion - Integrante 7

## 1. Que voy a presentar

En mi parte voy a explicar tres cosas:

- Como se usa el sistema desde consola.
- Que validaciones agregamos para evitar errores de entrada.
- Que documentacion deje lista para que cualquier companero pueda ejecutarlo.

Tiempo recomendado: 5 a 7 minutos.

---

## 2. Estructura de diapositivas (simple y clara)

### Diapositiva 1 - Mi rol en el proyecto

Texto sugerido:

"Yo fui el Integrante 7. Me encargue del menu de consola, manuales, validacion final y apoyo a la presentacion."

### Diapositiva 2 - Flujo de uso del programa

Texto sugerido:

"El flujo es directo: usuario -> menu -> evidencia -> inferencia -> resultado."

"La idea fue que cualquier persona pudiera usarlo sin saber detalles tecnicos del algoritmo."

### Diapositiva 3 - Mejoras que hice en el menu

Texto sugerido:

"Me enfoque en que el sistema no se rompiera por entradas incorrectas."

- Reintento si se elige una opcion invalida.
- Reintento si se escribe mal la evidencia.
- Opcion `0` para volver sin ejecutar la consulta.
- Mensajes claros para guiar al usuario.

### Diapositiva 4 - Demo corta

Mostrar rapido:

1. Opcion `3` (estructura de red).
2. Opcion `2` (escenarios).
3. Opcion `1` (consulta manual).
4. Ingresar un dato invalido para mostrar validacion.

### Diapositiva 5 - Manual de usuario

Ruta: `documentation/manual_usuario.md`

Texto sugerido:

"Aqui deje como ejecutar el proyecto, como usar el menu y como interpretar resultados."

### Diapositiva 6 - Manual tecnico

Ruta: `documentation/manual_tecnico.md`

Texto sugerido:

"Aqui explique la arquitectura por modulos y como extender nodos o escenarios."

### Diapositiva 7 - Validacion final

Ruta: `documentation/validacion_final.md`

Texto sugerido:

"Hice una validacion final para comprobar compilacion, ejecucion de escenarios y manejo de errores de entrada."

### Diapositiva 8 - Cierre

Texto sugerido:

"No solo buscamos que calcule probabilidades, tambien que sea facil de ejecutar, entender y mantener por el equipo."

---

## 3. Guion hablado (tono estudiante)

"En mi parte me enfoque en dejar el proyecto util de verdad para quien lo vaya a ejecutar. Mejore el menu para que valide entradas y no falle si el usuario se equivoca al escribir. Tambien deje listos el manual de usuario y el manual tecnico para que el equipo tenga una guia clara tanto de uso como de estructura interna. Finalmente hice una validacion final corriendo el proyecto desde cero para asegurar que todo funciona bien antes de la entrega."

---

## 4. Preguntas que nos pueden hacer

Pregunta: "Por que consola y no una web?"

Respuesta corta: "Porque el objetivo principal era demostrar inferencia bayesiana. La consola nos permitio enfocarnos en la logica del capitulo y no en frontend."

Pregunta: "Que pasa si el usuario no conoce un sintoma?"

Respuesta corta: "Puede poner `d` de desconocido y ese dato no se fuerza como evidencia."

Pregunta: "Como comprobaron que funciona?"

Respuesta corta: "Compilamos, ejecutamos escenarios y probamos errores de entrada para validar robustez."

---

## 5. Mensaje final para decir en clase

"Mi aporte fue cerrar la parte operativa del proyecto: uso real por consola, documentacion clara y validacion final. Asi el trabajo no solo queda correcto en teoria, sino tambien presentable y reproducible."
