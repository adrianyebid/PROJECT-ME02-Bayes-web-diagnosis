# Bayes Web Diagnosis

Sistema de diagnóstico probabilístico de fallas en aplicaciones web distribuidas mediante redes bayesianas.

Proyecto desarrollado para el curso de Inteligencia Artificial, basado en el **Capítulo 13: Probabilistic Reasoning** de *Artificial Intelligence: A Modern Approach* (Russell & Norvig).

---

## ¿Qué hace la aplicación?

Ante síntomas observados en una aplicación web distribuida (como errores HTTP 500, latencia alta o fallos de login), el sistema calcula la probabilidad de cada posible causa:

```
P(causa | síntoma_1 = valor, síntoma_2 = valor, ...)
```

Por ejemplo:

```
P(GatewayCaido | ServicioNoDisponible=si, LatenciaAlta=si, Error500=no) = 0.7320
P(BackendSaturado | Error500=si, ServicioNoDisponible=si, LatenciaAlta=si) = 0.5801
```

El motor de inferencia implementa desde cero el algoritmo **Enumeration-Ask** (inferencia exacta por enumeración) sin librerías externas de IA.

---

## Variables del modelo

**Causas** (variables ocultas a diagnosticar):

| Variable | Descripción | P(si) a priori |
|---|---|---|
| `BaseDatosCaida` | La base de datos presenta una falla activa | 0.05 |
| `BackendSaturado` | El servidor backend está sobrecargado | 0.10 |
| `GatewayCaido` | El API Gateway no está respondiendo | 0.04 |
| `ConexionInestable` | La red presenta intermitencia o pérdida de paquetes | 0.12 |
| `ErrorAutenticacion` | El servicio de autenticación tiene una falla activa | 0.08 |

**Síntomas** (evidencia observable que el usuario ingresa):

| Variable | Descripción |
|---|---|
| `Error500` | Error HTTP 500 en respuestas del servidor |
| `LatenciaAlta` | Tiempos de respuesta superiores al umbral normal |
| `LoginFallido` | Fallo en el proceso de inicio de sesión |
| `ServicioNoDisponible` | El servicio no responde en absoluto |
| `UsuarioAfectado` | El usuario final percibe degradación del servicio |

---

## Requisitos

- Python 3.8 o superior (recomendado 3.10+)
- `matplotlib` para generación de gráficas

```bash
pip install matplotlib
```

---

## Cómo ejecutar

```bash
python main.py
```

En Windows, si `python` no está configurado como `python3`:

```bash
python main.py
```

El programa presenta un menú interactivo con las siguientes opciones:

1. Realizar una consulta manual (seleccionar causa + ingresar evidencia)
2. Ejecutar los 5 escenarios de prueba predefinidos
3. Ejecutar análisis completo con gráficas comparativas
4. Salir

---

## Estructura del proyecto

```
bayes-web-diagnosis/
│
├── main.py               # Interfaz de consola y menú principal
├── node.py               # Clase Node: variable aleatoria booleana con CPT
├── bayesian_network.py   # Clase BayesianNetwork: contenedor del DAG
├── model.py              # Red bayesiana concreta con nodos y CPT del dominio
├── inference.py          # Algoritmo Enumeration-Ask y función normalize
├── scenarios.py          # 5 escenarios de prueba con análisis de sensibilidad
├── visualization.py      # Generación de gráficas comparativas
├── run_analysis.py       # Ejecución del análisis completo
├── utils.py              # Utilidades de parseo y formato
├── resultados_escenarios.json
│
├── graphs/               # Gráficas generadas por visualization.py
│   ├── comparacion_escenarios.png
│   ├── priori_vs_posteriori.png
│   ├── tiempos_ejecucion.png
│   ├── sensibilidad_completa.png
│   └── sensibilidad_<escenario>.png  (una por cada escenario)
│
├── images/
│   └── red-bayes.png     # Diagrama de clases del sistema
│
└── documentation/
    ├── marco_teorico.md
    ├── descripcion_problema.md
    ├── diseño_red_bayesiana.md
    ├── diseno_aplicacion.md
    ├── escenarios_prueba.md
    ├── manual_usuario.md
    ├── manual_tecnico.md
    └── validacion_final.md
```

---

## Resultados principales

| Escenario | Causa consultada | P(si) a priori | P(si \| evidencia) |
|---|---|---|---|
| E1 | BaseDatosCaida | 0.05 | 0.2824 |
| E2 | BackendSaturado | 0.10 | **0.5801** |
| E3 | ErrorAutenticacion | 0.08 | 0.4945 |
| E4 | ConexionInestable | 0.12 | 0.4573 |
| E5 | GatewayCaido | 0.04 | **0.7320** |

El escenario E5 (caída del gateway) es el más concluyente: la probabilidad posterior es 18 veces mayor que la a priori.

---

## Documentación

| Documento | Descripción |
|---|---|
| [Marco teórico](documentation/marco_teorico.md) | Fundamentos de redes bayesianas e inferencia probabilística (Cap. 13) |
| [Descripción del problema](documentation/descripcion_problema.md) | Contexto, variables del modelo y justificación |
| [Diseño de la red bayesiana](documentation/diseño_red_bayesiana.md) | Estructura del DAG y tablas CPT |
| [Diseño de la aplicación](documentation/diseno_aplicacion.md) | Arquitectura de módulos y diagramas de clases y secuencia |
| [Escenarios de prueba](documentation/escenarios_prueba.md) | Definición, ejecución y análisis de los 5 escenarios con gráficas |
| [Manual de usuario](documentation/manual_usuario.md) | Guía paso a paso para ejecutar y usar el sistema |
| [Manual técnico](documentation/manual_tecnico.md) | Referencia interna de implementación para mantenimiento |
| [Validación final](documentation/validacion_final.md) | Verificación de correctitud, normalizacion y robustez |

---

## Equipo

| Integrante | Rol |
|---|---|
| Tomas Felipe Garzon Gomez | Coordinación general y definición del problema |
| Camilo Borja Rojas | Implementación de clases base (`node.py`, `bayesian_network.py`) |
| Tomás Sebastián Vallejo Fonseca | Diseño del modelo probabilístico y tablas CPT (`model.py`) |
| Javier Santiago Giraldo Jiménez | Marco teórico y módulo de visualización |
| Adrian Yebid Rincon | Motor de inferencia y validaciones (`inference.py`) |
| David Felipe Chaparro Pérez | Escenarios de prueba y análisis de resultados (`scenarios.py`) |
| Pablo Felipe Sandoval Menjura | Manuales, menú de consola y validación final |
