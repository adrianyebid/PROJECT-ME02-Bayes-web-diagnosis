# Bayes Web Diagnosis

## Sistema bayesiano para el diagnóstico probabilístico de fallas en una aplicación web distribuida

Este proyecto consiste en el desarrollo de una aplicación de software que permite estimar probabilísticamente la causa más probable de una falla en una aplicación web distribuida, utilizando redes bayesianas e inferencia probabilística.

El proyecto se basa en el Capítulo 13: Probabilistic Reasoning del libro Artificial Intelligence: A Modern Approach, de Stuart Russell y Peter Norvig. En este capítulo se estudia cómo representar conocimiento incierto mediante redes bayesianas, tablas de probabilidad condicional e inferencia probabilística.

La aplicación no se conecta a un sistema real externo. En su lugar, simula el comportamiento de una aplicación web distribuida mediante variables probabilísticas. A partir de síntomas observados, como error 500, latencia alta, login fallido o servicio no disponible, el sistema calcula la probabilidad de distintas causas posibles, como caída de base de datos, backend saturado, gateway caído, conexión inestable o error de autenticación.

---

## Planteamiento del problema

En una aplicación web distribuida pueden ocurrir fallas en diferentes componentes, como el backend, la base de datos, el API Gateway, el servicio de autenticación o la red. El problema es que muchas veces los síntomas observados son similares y no permiten identificar directamente la causa real.

Por ejemplo, una latencia alta puede deberse a una conexión inestable, a un backend saturado o a una base de datos lenta. De igual forma, un error 500 puede originarse por una falla interna del servidor, una caída de la base de datos o saturación del backend.

Por esta razón, el objetivo del proyecto es construir un sistema capaz de responder preguntas como:

P(BaseDatosCaida | Error500 = sí, LatenciaAlta = sí)

Es decir, calcular la probabilidad de que una causa sea verdadera dado un conjunto de evidencias observadas.

---

## Objetivo general

Desarrollar una aplicación en Python que implemente una red bayesiana desde cero para diagnosticar probabilísticamente fallas en una aplicación web distribuida, a partir de síntomas observables ingresados por el usuario o definidos en escenarios de prueba.

---

## Objetivos específicos

* Modelar un problema de diagnóstico de fallas usando una red bayesiana.
* Definir variables aleatorias booleanas para representar causas y síntomas.
* Construir tablas de probabilidad condicional para cada nodo de la red.
* Implementar desde cero el algoritmo de inferencia por enumeración.
* Calcular consultas probabilísticas de la forma P(X | evidencia).
* Normalizar los resultados para obtener distribuciones de probabilidad válidas.
* Probar el sistema con al menos tres escenarios representativos.
* Analizar cómo cambian las probabilidades según la evidencia observada.

---

## Lenguaje de implementación

El proyecto se implementará en:

Python 3

Se usará Python porque permite trabajar fácilmente con estructuras de datos como listas, diccionarios, tuplas y clases. Además, permite implementar los algoritmos probabilísticos desde cero sin depender de librerías externas que ya resuelvan el problema.

---

## Librerías permitidas

Se propone usar únicamente librerías estándar de Python:

* itertools: para generar combinaciones de variables ocultas.
* time: para medir tiempos de ejecución en los escenarios de prueba.
* json: opcional, para guardar o cargar escenarios.

No se usarán librerías como pgmpy, pomegranate, scikit-learn, numpy, pandas, networkx, TensorFlow o PyTorch, porque algunas de ellas ya implementan modelos probabilísticos, estructuras de grafos o herramientas que podrían resolver parte del problema.

---

## Modelo bayesiano propuesto

La red bayesiana tendrá variables booleanas, es decir, cada variable podrá tomar los valores:

* sí
* no

### Variables causa

Estas variables representan posibles causas internas de una falla:

* BaseDatosCaida
* BackendSaturado
* GatewayCaido
* ConexionInestable
* ErrorAutenticacion

### Variables síntoma

Estas variables representan síntomas observables por el usuario o por el sistema:

* Error500
* LatenciaAlta
* LoginFallido
* ServicioNoDisponible
* UsuarioAfectado

---

## Estructura causal de la red

La red bayesiana propuesta tiene la siguiente estructura:

BaseDatosCaida y BackendSaturado influyen sobre Error500.

GatewayCaido y ConexionInestable influyen sobre LatenciaAlta.

ErrorAutenticacion influye sobre LoginFallido.

Error500 y LatenciaAlta influyen sobre UsuarioAfectado.

GatewayCaido, BackendSaturado y BaseDatosCaida influyen sobre ServicioNoDisponible.

Representación simplificada:

BaseDatosCaida ─────┐
├── Error500 ─────┐
BackendSaturado ────┘                 │
├── UsuarioAfectado
GatewayCaido ───────┐                 │
├── LatenciaAlta ─┘
ConexionInestable ──┘

ErrorAutenticacion ─────────────── LoginFallido

GatewayCaido ───────────────────── ServicioNoDisponible
BackendSaturado ────────────────── ServicioNoDisponible
BaseDatosCaida ─────────────────── ServicioNoDisponible

---

## Qué se va a implementar

El proyecto tendrá los siguientes componentes principales:

### 1. Representación de nodos

Se implementará una clase Node para representar cada variable de la red bayesiana.

Cada nodo tendrá:

* Nombre de la variable.
* Lista de padres.
* Tabla de probabilidad condicional.
* Método para consultar la probabilidad local según la evidencia.

### 2. Representación de la red bayesiana

Se implementará una clase BayesianNetwork para almacenar todos los nodos de la red.

La red tendrá:

* Diccionario de nodos.
* Orden topológico de las variables.
* Métodos para agregar nodos.
* Métodos para consultar nodos y probabilidades.

### 3. Tablas de probabilidad condicional

Cada nodo tendrá una tabla CPT que indica la probabilidad de que la variable sea verdadera según el estado de sus padres.

Ejemplo:

Nodo: Error500
Padres: BaseDatosCaida, BackendSaturado

BaseDatosCaida | BackendSaturado | P(Error500 = sí)
sí              | sí              | 0.95
sí              | no              | 0.85
no              | sí              | 0.70
no              | no              | 0.05

### 4. Motor de inferencia

Se implementará desde cero el algoritmo de inferencia por enumeración.

Este algoritmo permitirá calcular consultas como:

P(BaseDatosCaida | Error500 = sí, LatenciaAlta = sí)

P(BackendSaturado | Error500 = sí, ServicioNoDisponible = sí)

P(ErrorAutenticacion | LoginFallido = sí)

P(ConexionInestable | LatenciaAlta = sí, Error500 = no)

### 5. Normalización de resultados

Después de calcular los valores no normalizados para cada posible valor de la variable consultada, el sistema normalizará los resultados para que la suma de probabilidades sea igual a 1.

Ejemplo de salida:

BaseDatosCaida = sí: 0.64
BaseDatosCaida = no: 0.36

### 6. Menú de consola

La aplicación tendrá un menú por consola que permitirá:

* Seleccionar la variable que se desea consultar.
* Ingresar evidencia observada.
* Ejecutar la inferencia.
* Mostrar los resultados.
* Ejecutar escenarios de prueba predefinidos.

### 7. Escenarios de prueba

Se implementarán escenarios representativos para validar el funcionamiento del sistema y analizar cómo cambian las probabilidades según la evidencia.

---

## Escenarios de prueba propuestos

### Escenario 1: posible caída de base de datos

Evidencia:

* Error500 = sí
* LatenciaAlta = sí
* LoginFallido = no

Consulta:

P(BaseDatosCaida | Error500 = sí, LatenciaAlta = sí, LoginFallido = no)

Resultado esperado:

La probabilidad de BaseDatosCaida debe aumentar, porque existe error interno y lentitud en el sistema.

---

### Escenario 2: backend saturado

Evidencia:

* Error500 = sí
* ServicioNoDisponible = sí
* LatenciaAlta = sí

Consulta:

P(BackendSaturado | Error500 = sí, ServicioNoDisponible = sí, LatenciaAlta = sí)

Resultado esperado:

La probabilidad de BackendSaturado debe ser alta, porque hay varios síntomas asociados a sobrecarga o falla interna.

---

### Escenario 3: problema de autenticación

Evidencia:

* LoginFallido = sí
* Error500 = no
* LatenciaAlta = no

Consulta:

P(ErrorAutenticacion | LoginFallido = sí, Error500 = no, LatenciaAlta = no)

Resultado esperado:

La probabilidad de ErrorAutenticacion debe aumentar, porque el problema se concentra en el inicio de sesión y no en el rendimiento general del sistema.

---

### Escenario 4: problema de red o conexión

Evidencia:

* LatenciaAlta = sí
* Error500 = no
* ServicioNoDisponible = no

Consulta:

P(ConexionInestable | LatenciaAlta = sí, Error500 = no, ServicioNoDisponible = no)

Resultado esperado:

La probabilidad de ConexionInestable debe aumentar, porque hay lentitud, pero no hay señales claras de una falla interna del backend o de la base de datos.

---

### Escenario 5: caída del gateway

Evidencia:

* ServicioNoDisponible = sí
* LatenciaAlta = sí
* Error500 = no

Consulta:

P(GatewayCaido | ServicioNoDisponible = sí, LatenciaAlta = sí, Error500 = no)

Resultado esperado:

La probabilidad de GatewayCaido debe subir, porque el servicio no está disponible y hay latencia, pero no se presenta error interno del servidor.

---

## Estructura del repositorio

bayes-web-diagnosis/
│
├── main.py
├── node.py
├── bayesian_network.py
├── inference.py
├── scenarios.py
├── README.md
│
└── documentation/
├── marco_teorico.md
├── descripcion_problema.md
├── diseno_aplicacion.md
├── manual_usuario.md
├── manual_tecnico.md
└── escenarios_prueba.md

---

## Descripción de archivos

### main.py

Archivo principal del programa. Contiene el menú de consola y permite ejecutar consultas o escenarios de prueba.

### node.py

Contiene la clase Node, encargada de representar cada variable aleatoria de la red bayesiana.

### bayesian_network.py

Contiene la clase BayesianNetwork, encargada de almacenar los nodos, el orden topológico y la estructura general de la red.

### inference.py

Contiene el algoritmo de inferencia por enumeración, la función de normalización y las funciones auxiliares para calcular probabilidades.

### scenarios.py

Contiene los escenarios de prueba predefinidos para validar el sistema.

### documentation/

Carpeta destinada a la documentación del proyecto, incluyendo marco teórico, diseño, manuales y escenarios de prueba.

---

## División del trabajo

El grupo está conformado por 7 integrantes. La división se propone de forma equitativa, procurando que cada integrante tenga una parte conceptual y una parte práctica.

---

## Integrante 1: Coordinación general y planteamiento del problema

Responsabilidades:

* Redactar el planteamiento del problema.
* Justificar por qué el problema pertenece al área de computación.
* Definir el alcance del proyecto.
* Coordinar la integración del informe final.
* Revisar que todos los documentos tengan coherencia y el mismo estilo.

Parte práctica:

* Apoyar la definición de las variables principales del modelo.
* Validar que los escenarios de prueba estén conectados con el problema.

Descripción del rol:

Este integrante se encargará de la definición general del problema, la justificación del dominio de aplicación y la integración final del informe.

---

## Integrante 2: Marco teórico del capítulo 13

Responsabilidades:

* Redactar el marco teórico.
* Explicar el concepto de razonamiento probabilístico.
* Explicar redes bayesianas.
* Explicar tablas de probabilidad condicional.
* Explicar independencia condicional.
* Explicar inferencia por enumeración.

Parte práctica:

* Verificar que el algoritmo implementado corresponda al explicado en el capítulo.
* Relacionar las fórmulas del capítulo con el código desarrollado.

Descripción del rol:

Este integrante se encargará del soporte teórico del proyecto y de validar que la solución esté realmente basada en los conceptos del capítulo asignado.

---

## Integrante 3: Diseño de la red bayesiana y tablas CPT

Responsabilidades:

* Diseñar la estructura de la red bayesiana.
* Definir los nodos causa y los nodos síntoma.
* Definir los padres de cada nodo.
* Crear las tablas de probabilidad condicional.
* Verificar que las probabilidades sean coherentes.

Parte práctica:

* Implementar o cargar las CPT dentro del código.
* Probar que cada nodo devuelva correctamente sus probabilidades locales.

Descripción del rol:

Este integrante se encargará del diseño probabilístico del modelo, incluyendo variables aleatorias, dependencias causales y tablas de probabilidad condicional.

---

## Integrante 4: Implementación de estructuras base

Responsabilidades:

* Implementar la clase Node.
* Implementar la clase BayesianNetwork.
* Crear métodos para agregar nodos a la red.
* Crear métodos para consultar padres y probabilidades locales.
* Mantener el orden topológico de las variables.

Parte documental:

* Documentar la estructura técnica del código.
* Explicar cómo se representa internamente la red bayesiana.

Descripción del rol:

Este integrante se encargará de construir la base técnica sobre la cual funcionará el sistema bayesiano.

---

## Integrante 5: Implementación del algoritmo de inferencia

Responsabilidades:

* Implementar la función enumeration_ask.
* Implementar la función enumerate_all.
* Implementar la función probability.
* Implementar la función normalize.
* Validar que los resultados de probabilidad sumen 1.

Parte documental:

* Explicar paso a paso el algoritmo de inferencia utilizado.
* Relacionar el algoritmo con el capítulo del libro.

Descripción del rol:

Este integrante se encargará del motor principal de inferencia probabilística del sistema.

---

## Integrante 6: Escenarios de prueba y análisis de resultados

Responsabilidades:

* Diseñar mínimo tres escenarios de prueba.
* Ejecutar el programa con diferentes evidencias.
* Registrar los resultados obtenidos.
* Analizar cómo cambian las probabilidades según la evidencia.
* Comparar los resultados entre escenarios.

Parte práctica:

* Crear el archivo scenarios.py.
* Automatizar la ejecución de escenarios.
* Medir tiempos de ejecución si se usa la librería time.

Descripción del rol:

Este integrante se encargará de la validación experimental del sistema y del análisis de resultados.

---

## Integrante 7: Manuales, menú de consola y validación final

Responsabilidades:

* Crear el manual de usuario.
* Crear el manual técnico.
* Preparar la presentación o apoyo para exposición.
* Revisar ortografía y formato.
* Verificar que el proyecto corra desde cero.

Parte práctica:

* Implementar o mejorar el menú de consola.
* Validar la experiencia de uso.
* Controlar errores básicos de entrada del usuario.

Descripción del rol:

Este integrante se encargará de la interacción con el usuario, los manuales y la validación final del aplicativo.

---

## Tabla resumida de roles

| Integrante   | Rol principal           | Parte conceptual              | Parte práctica                    |
| ------------ | ----------------------- | ----------------------------- | --------------------------------- |
| Integrante 1 | Coordinación y problema | Planteamiento y justificación | Definición de alcance y variables |
| Integrante 2 | Marco teórico           | Redes bayesianas e inferencia | Validación teórica del algoritmo  |
| Integrante 3 | Modelo probabilístico   | Diseño de nodos y CPT         | Carga de probabilidades           |
| Integrante 4 | Estructuras base        | Manual técnico de clases      | Node y BayesianNetwork            |
| Integrante 5 | Inferencia              | Explicación del algoritmo     | enumeration_ask y normalize       |
| Integrante 6 | Pruebas                 | Análisis de resultados        | scenarios.py y ejecución          |
| Integrante 7 | Manuales y presentación | Manual usuario/técnico        | Menú de consola y validación      |

---

## Entregables esperados

El proyecto incluirá los siguientes entregables:

* Marco teórico.
* Descripción y justificación del problema.
* Diseño de la aplicación.
* Código fuente completo.
* Manual de usuario.
* Manual técnico.
* Documentación de al menos tres escenarios de prueba.
* Análisis de resultados.
* Repositorio con el código y la documentación.

---

## Estado inicial del proyecto

Este repositorio inicia con la planeación del proyecto, la definición del problema, la estructura de la red bayesiana, la división de tareas y la organización inicial del código fuente.

---

## Resultado esperado

Al finalizar el proyecto, se espera contar con una aplicación funcional por consola que permita ingresar evidencias observadas y obtener probabilidades posteriores sobre posibles causas de fallas en una aplicación web distribuida.

Ejemplo de resultado esperado:

Consulta:

P(BaseDatosCaida | Error500 = sí, LatenciaAlta = sí)

Salida:

BaseDatosCaida = sí: 0.64
BaseDatosCaida = no: 0.36

Interpretación:

Según la evidencia observada, el sistema estima que existe una probabilidad alta de que la base de datos esté caída.

---

## Conclusión

Bayes Web Diagnosis busca aplicar los conceptos de razonamiento probabilístico y redes bayesianas a un problema práctico del área de computación. La solución se centra en construir desde cero un motor de inferencia capaz de trabajar con incertidumbre, calcular probabilidades condicionadas y apoyar el diagnóstico de fallas en sistemas distribuidos.
