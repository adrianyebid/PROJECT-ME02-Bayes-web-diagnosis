# PARTE CONCEPTUAL — INTEGRANTE 1

**Proyecto:** Sistema bayesiano para el diagnóstico probabilístico de fallas en una aplicación web distribuida
**Capítulo de referencia:** Capítulo 13 — *Probabilistic Reasoning* (Russell & Norvig, *Artificial Intelligence: A Modern Approach*)

---

# 1. DESCRIPCIÓN Y PLANTEAMIENTO DEL PROBLEMA

## 1.1 Contexto

Las aplicaciones web modernas rara vez se ejecutan como un único programa monolítico. En su lugar, adoptan arquitecturas distribuidas en las que múltiples componentes especializados cooperan para atender cada solicitud del usuario: un frontend que renderiza la interfaz en el navegador, un API Gateway que enruta y valida las peticiones entrantes, uno o varios servicios de backend que ejecutan la lógica de negocio, un servicio de autenticación que gestiona sesiones y permisos, una o varias bases de datos que almacenan el estado persistente, y una infraestructura de red que interconecta todos estos elementos. Esta arquitectura ofrece ventajas conocidas en escalabilidad, mantenibilidad y resiliencia, pero introduce un costo operativo importante: la dificultad para diagnosticar fallas cuando algo deja de funcionar.

A diferencia de un sistema monolítico, donde un fallo suele rastrearse a una porción específica de código, en un sistema distribuido la causa de una falla puede estar en cualquiera de los componentes, en la comunicación entre ellos, o en una combinación de varios factores simultáneos. Y lo más relevante para este proyecto: el operador del sistema rara vez observa la causa directamente. Lo que observa son los síntomas.

## 1.2 El problema

Cuando un usuario reporta que la aplicación no funciona, o cuando una herramienta de monitoreo emite una alerta, la información disponible casi siempre tiene la forma de manifestaciones externas: un error HTTP 500, una respuesta lenta, un intento de inicio de sesión fallido, un servicio que devuelve 503. Estos síntomas son la única evidencia con la que el operador cuenta para decidir qué componente revisar primero, qué servicio reiniciar, o a qué equipo escalar el incidente.

El problema de fondo es que la relación entre síntomas y causas es ambigua. Un mismo síntoma puede ser producido por varias causas distintas, y una misma causa puede manifestarse a través de varios síntomas. Por ejemplo, una latencia elevada puede deberse a una base de datos lenta, a un backend saturado, a una red con pérdida de paquetes, o a una combinación de estos factores. Inversamente, una caída de la base de datos puede manifestarse simultáneamente como errores 500, como servicios no disponibles y como reportes de usuarios afectados. Esta ambigüedad de muchos a muchos hace que el diagnóstico no pueda resolverse mediante reglas deterministas simples del tipo "si el síntoma es X, entonces la causa es Y".

Adicionalmente, el operador rara vez dispone de información completa. En un incidente real, algunos síntomas se conocen, otros no se han verificado, y otros pueden no haberse manifestado todavía. La decisión sobre qué componente investigar debe tomarse con evidencia parcial y bajo presión de tiempo, ya que cada minuto que el sistema permanece degradado tiene un costo económico y de reputación.

## 1.3 Por qué este problema requiere razonamiento bajo incertidumbre

Tres características hacen que este problema no pueda abordarse con métodos puramente deductivos.

Primero, la información es incompleta por naturaleza. No existe acceso instantáneo al estado interno de todos los componentes; lo que se tiene son observaciones indirectas de su comportamiento.

Segundo, las relaciones entre causas y síntomas no son determinísticas. Una base de datos caída no siempre produce un error 500 visible, y un error 500 no siempre proviene de la base de datos. Lo que existe es una probabilidad —empíricamente conocida por los ingenieros con experiencia— de que ciertas causas produzcan ciertos efectos.

Tercero, las causas pueden coexistir o reforzarse entre sí. Un sistema bajo alta carga puede tener simultáneamente backend saturado, latencia elevada y errores intermitentes, sin que ninguno sea "la" causa única.

En conjunto, estas tres características describen el escenario clásico en el que el razonamiento probabilístico es la herramienta apropiada: hay variables aleatorias (las causas y los síntomas), hay observaciones parciales (la evidencia), hay relaciones probabilísticas entre ellas (las CPT), y la pregunta operativa relevante puede formularse como una probabilidad condicional.

## 1.4 Formulación formal del problema

Sea C = {C₁, C₂, ..., Cₙ} el conjunto de variables que representan posibles causas de falla en los componentes del sistema (base de datos caída, backend saturado, gateway caído, conexión inestable, error de autenticación). Sea S = {S₁, S₂, ..., Sₘ} el conjunto de variables que representan síntomas observables (error 500, latencia alta, login fallido, servicio no disponible, usuario afectado). Todas las variables son booleanas: cada una toma el valor verdadero o falso.

Dada una observación parcial e ⊆ S, donde el operador conoce el valor de algunos síntomas y deja otros como desconocidos, el problema consiste en calcular la distribución de probabilidad posterior

> P(Cᵢ | e)

para cada causa Cᵢ ∈ C de interés. La causa con mayor probabilidad posterior es la hipótesis más plausible y, por lo tanto, el primer candidato a investigar.

Formalmente, este cálculo se apoya en la regla de Bayes y en la factorización compacta de la distribución conjunta que ofrece una red bayesiana:

> P(X₁, ..., Xₖ) = ∏ P(Xᵢ | Padres(Xᵢ))

donde Xᵢ recorre todas las variables del modelo. La ventaja de esta factorización, demostrada en el Capítulo 13 de Russell y Norvig, es que reduce drásticamente la cantidad de parámetros necesarios respecto a la distribución conjunta completa, gracias a las independencias condicionales codificadas en el grafo.

## 1.5 Ejemplo ilustrativo

Considérese el siguiente caso. Un operador recibe la siguiente evidencia desde el sistema de monitoreo: el servidor está devolviendo errores 500 con frecuencia inusual y la latencia promedio se ha elevado por encima del umbral aceptable. No se han reportado fallos de inicio de sesión.

Con esta evidencia, varias hipótesis son compatibles. Podría tratarse de una caída parcial de la base de datos, lo que explicaría tanto los errores 500 como el aumento de latencia. Podría tratarse de un backend saturado, que también produce ambos efectos. Podría incluso tratarse de una combinación de los dos. Sin más información, el operador no puede distinguir entre estas posibilidades con certeza.

El sistema propuesto en este proyecto resuelve precisamente este escenario: dada la evidencia ingresada por el operador, calcula la probabilidad posterior de cada causa y permite identificar cuál es la hipótesis más plausible, junto con su grado de confianza relativo. Si por ejemplo el cálculo arroja P(BaseDatosCaida | evidencia) = 0.64 y P(BackendSaturado | evidencia) = 0.41, el operador sabe por dónde comenzar la investigación, sin descartar la segunda hipótesis.

## 1.6 Pregunta de investigación

El proyecto se orienta a responder la siguiente pregunta:

> ¿Es posible construir un sistema, basado en una red bayesiana implementada desde cero, que estime de forma probabilística la causa más probable de una falla en una aplicación web distribuida a partir de un conjunto parcial de síntomas observados, y que produzca resultados coherentes con el razonamiento que un operador experimentado realizaría intuitivamente?

Responder afirmativamente esta pregunta implica diseñar la red, parametrizar las tablas de probabilidad condicional con criterio ingenieril, implementar el algoritmo de inferencia exacta por enumeración descrito en el Capítulo 13, y validar su comportamiento mediante escenarios de prueba representativos.

---

# 2. JUSTIFICACIÓN

## 2.1 El problema pertenece al dominio de la computación

El diagnóstico de fallas en aplicaciones web distribuidas es un problema central de la ingeniería de software y de la administración de sistemas. Una aplicación web distribuida moderna se compone de múltiples capas que cooperan para atender una solicitud del usuario: el frontend renderiza la interfaz, el API Gateway enruta y valida solicitudes, el backend ejecuta la lógica de negocio, los servicios de autenticación gestionan sesiones y permisos, las bases de datos almacenan el estado persistente, y la red interconecta todos estos componentes. Cuando alguno de estos elementos falla o se degrada, el efecto rara vez se manifiesta de forma directa en el componente afectado: lo que el usuario percibe son síntomas como errores HTTP, latencia elevada, imposibilidad de iniciar sesión o servicios que no responden.

Este escenario plantea un problema técnico genuino del área de computación porque el objeto de estudio son artefactos de software y su comportamiento operativo; porque diagnosticar fallas es una tarea cotidiana en operaciones de sistemas (DevOps, SRE), apoyada actualmente en herramientas como sistemas de monitoreo, registros centralizados y plataformas de alertas; y porque la toma de decisiones bajo incertidumbre sobre el estado de un sistema computacional es objeto de investigación activa en áreas como observabilidad, diagnóstico automatizado y mantenimiento predictivo de software.

Resolver este problema, incluso parcialmente, tiene valor práctico: reduce el tiempo medio de detección de fallas, disminuye la dependencia del conocimiento tácito del personal experimentado y permite priorizar acciones correctivas cuando varios componentes podrían estar comprometidos al mismo tiempo.

## 2.2 El razonamiento probabilístico es la herramienta adecuada

La razón por la cual el Capítulo 13 del libro *Artificial Intelligence: A Modern Approach* de Stuart Russell y Peter Norvig se ajusta naturalmente a este problema radica en tres características del dominio.

**Existe incertidumbre estructural.** Cuando un usuario reporta una falla, el operador rara vez tiene acceso inmediato al estado interno de todos los componentes. Las observaciones disponibles son los síntomas; las causas son ocultas o parcialmente observables. Esta es la situación típica que justifica el razonamiento probabilístico frente al razonamiento lógico clásico: no es posible deducir con certeza cuál fue la causa, pero sí estimar qué tan probable es cada hipótesis dada la evidencia.

**Las relaciones entre variables son causales y conocidas.** Aunque la causa exacta es incierta, el conocimiento ingenieril sobre la arquitectura del sistema permite especificar qué causas pueden producir qué síntomas. Una base de datos caída puede generar errores 500, pero no genera directamente fallas de autenticación si el servicio de auth tiene su propia infraestructura. Estas dependencias estructurales se modelan exactamente con un grafo acíclico dirigido, donde cada arista expresa una influencia causal directa, tal como describen Russell y Norvig en la sección dedicada a la semántica de las redes bayesianas.

**La consulta de interés es una probabilidad posterior.** La pregunta operativa "dados estos síntomas, ¿cuál es la causa más probable?" se traduce formalmente en el cálculo de P(Causa | Evidencia), que es precisamente la consulta canónica resuelta mediante inferencia bayesiana. El capítulo describe el algoritmo de inferencia por enumeración como método exacto para responder este tipo de consultas, con normalización final para obtener una distribución de probabilidad válida.

## 2.3 Conceptos del capítulo aplicados al proyecto

La solución propuesta utiliza, de forma directa y verificable, los siguientes elementos del Capítulo 13: variables aleatorias booleanas para representar causas y síntomas; un grafo acíclico dirigido para representar dependencias causales; tablas de probabilidad condicional (CPT) que parametrizan P(nodo | padres) para cada nodo; el principio de independencia condicional, que justifica la ausencia de aristas entre variables no relacionadas directamente y reduce drásticamente la cantidad de parámetros a especificar; la distribución conjunta factorizada según la regla de la cadena para redes bayesianas, P(X₁,...,Xₙ) = ∏ P(Xᵢ | Padres(Xᵢ)); la inferencia exacta por enumeración como algoritmo principal para calcular P(Consulta | Evidencia); y la normalización del vector resultante para obtener una distribución válida.

Más del cincuenta por ciento del esfuerzo técnico del proyecto se concentra en la implementación y validación de estos componentes, lo cual cumple con el requisito establecido en el enunciado de la asignación de que la mayor parte de la solución dependa del capítulo asignado.

---

# 3. ALCANCE Y VARIABLES DEL PROYECTO

## 3.1 Alcance del proyecto

### 3.1.1 Lo que el sistema sí hace

El sistema modela una red bayesiana fija con diez variables aleatorias booleanas que representan causas y síntomas frecuentes en una aplicación web distribuida. Permite al usuario ingresar evidencia parcial —síntomas observados, no observados o de valor desconocido— a través de una interfaz por consola. Calcula la probabilidad posterior P(VariableConsulta | Evidencia) mediante inferencia exacta por enumeración, normaliza los resultados y los presenta junto con una interpretación textual. Incluye al menos cinco escenarios de prueba documentados que ilustran distintos tipos de falla (base de datos, backend, autenticación, red y gateway), y provee manuales de usuario y técnico que permiten reproducir, entender y extender el sistema.

### 3.1.2 Lo que el sistema no hace

El sistema no aprende parámetros a partir de datos reales: las probabilidades de las CPT se establecen manualmente con base en criterio ingenieril. No se conecta con sistemas reales de monitoreo, log management o alertas. No implementa inferencia aproximada (muestreo de Gibbs, rejection sampling, likelihood weighting); la inferencia es exclusivamente exacta por enumeración. No utiliza variables continuas ni temporales: todas las variables son booleanas y la red no es dinámica. No incluye interfaz gráfica web ni de escritorio: la interacción es por consola. No incluye autenticación de usuarios, persistencia en base de datos ni despliegue como servicio.

### 3.1.3 Limitaciones técnicas asumidas

La red se considera estática: la estructura del DAG y los valores de las CPT no cambian durante la ejecución. Se asume independencia condicional entre nodos no conectados directamente. Los valores numéricos de las CPT son una aproximación didáctica y no provienen de mediciones empíricas sobre sistemas reales. La inferencia por enumeración es exponencial en el número de variables ocultas, por lo que el sistema está diseñado y dimensionado para diez variables y no pretende escalar a redes arbitrariamente grandes.

## 3.2 Variables del modelo

El sistema utiliza diez variables aleatorias booleanas, divididas en dos grupos: causas, que corresponden a estados internos no directamente observables del sistema, y síntomas, que son manifestaciones observables por el usuario o el sistema de monitoreo.

### 3.2.1 Variables causa

Representan posibles estados de falla en componentes del sistema. Son las hipótesis que el motor de inferencia evalúa al recibir evidencia.

| Variable | Descripción |
|---|---|
| BaseDatosCaida | La base de datos no responde correctamente a las consultas del backend |
| BackendSaturado | El backend está sobrecargado y no procesa solicitudes en tiempo aceptable |
| GatewayCaido | El API Gateway no enruta correctamente las solicitudes entrantes |
| ConexionInestable | La red presenta pérdida de paquetes, latencia elevada o cortes intermitentes |
| ErrorAutenticacion | El servicio de autenticación rechaza credenciales válidas o no responde |

### 3.2.2 Variables síntoma

Representan manifestaciones observables que el operador o el usuario pueden reportar como evidencia para alimentar el motor de inferencia.

| Variable | Descripción |
|---|---|
| Error500 | El servidor responde con código HTTP 500 (Internal Server Error) |
| LatenciaAlta | El tiempo de respuesta excede umbrales aceptables (mayor a dos segundos) |
| LoginFallido | El usuario no logra iniciar sesión a pesar de usar credenciales válidas |
| ServicioNoDisponible | El sistema no responde o devuelve códigos 503/504 |
| UsuarioAfectado | Un usuario final reporta que la aplicación no funciona correctamente |

### 3.2.3 Justificación de la selección de variables

Las variables seleccionadas cumplen tres criterios. Primero, son representativas de fallas y síntomas reales en arquitecturas web distribuidas: cualquier ingeniero de operaciones reconoce los términos como problemas que efectivamente ocurren en producción. Segundo, son observables o diagnosticables en entornos reales mediante herramientas de monitoreo estándar como logs centralizados, health checks y métricas de latencia, lo cual hace que el modelo, aunque didáctico, no sea artificial. Tercero, son suficientes para ilustrar dependencias causales no triviales —incluyendo casos donde varias causas convergen en un mismo síntoma, como Error500 que depende tanto de BaseDatosCaida como de BackendSaturado— sin que el modelo se vuelva computacionalmente intratable.

El número de variables se acotó intencionalmente en diez. Una red con muchas más variables haría que la inferencia por enumeración fuera lenta de demostrar y de explicar en clase, mientras que un número menor no permitiría ilustrar relaciones causales múltiples ni la riqueza del razonamiento bayesiano que se busca evidenciar en el proyecto.
