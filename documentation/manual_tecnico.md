# Manual tecnico

## 1. Objetivo tecnico

Este documento resume como esta construido **Bayes Web Diagnosis** por dentro, para que el equipo lo pueda mantener y extender sin perder tiempo.

---

## 2. Arquitectura general

El sistema esta organizado en modulos desacoplados:

- `node.py`: define cada variable aleatoria como nodo de red bayesiana.
- `bayesian_network.py`: administra nodos, orden topologico y consultas de probabilidad local.
- `model.py`: construye la red concreta del dominio web-diagnosis (nodos + CPT).
- `inference.py`: implementa inferencia exacta por enumeracion.
- `scenarios.py`: contiene escenarios de prueba y ejecucion automatizada.
- `utils.py`: utilidades de parseo, formato y salida.
- `main.py`: interfaz de consola y orquestacion del flujo de uso.

Idea general:
Separamos logica probabilistica, modelo y consola para que cada parte del grupo pudiera trabajar sin bloquear a los demas.

---

## 3. Modelo de datos

### 3.1 Clase `Node`

Responsabilidades:

- Guardar nombre, padres y CPT.
- Validar consistencia de CPT al instanciar (`validate_cpt`).
- Retornar probabilidad local `P(X=value | padres)`.

Estructura de CPT:

- Llave: tupla booleana con valores de padres en el orden definido.
- Valor: `P(Node=True | padres)`.

Reglas de validacion:

- Numero de filas debe ser `2^n`, donde `n` es cantidad de padres.
- Longitud de cada llave debe coincidir con `n`.
- Cada probabilidad debe estar en `[0, 1]`.

### 3.2 Clase `BayesianNetwork`

Responsabilidades:

- Registrar nodos (`add_node`).
- Mantener orden de evaluacion (`order`).
- Validar que todos los padres existan (`validate_network`).
- Delegar probabilidad local a cada nodo (`probability`).

Nota: el algoritmo de enumeracion asume que `order` respeta causalidad (padres antes que hijos).

---

## 4. Red bayesiana implementada (`model.py`)

Variables causa:

- `BaseDatosCaida`
- `BackendSaturado`
- `GatewayCaido`
- `ConexionInestable`
- `ErrorAutenticacion`

Variables sintoma:

- `Error500` depende de `BaseDatosCaida`, `BackendSaturado`
- `LatenciaAlta` depende de `GatewayCaido`, `ConexionInestable`
- `LoginFallido` depende de `ErrorAutenticacion`
- `ServicioNoDisponible` depende de `GatewayCaido`, `BackendSaturado`, `BaseDatosCaida`
- `UsuarioAfectado` depende de `Error500`, `LatenciaAlta`

---

## 5. Motor de inferencia (`inference.py`)

### 5.1 Funcion `enumeration_ask(query, evidence, network)`

Implementa la consulta posterior:

`P(query | evidence)`

Flujo:

1. Verifica que `query` no este incluida en evidencia.
2. Construye distribucion no normalizada para `query=True` y `query=False`.
3. Para cada caso llama `enumerate_all(...)`.
4. Aplica `normalize(...)`.

### 5.2 Funcion `enumerate_all(variables, evidence, network)`

Implementacion recursiva de enumeracion exacta.

Casos:

- Si no quedan variables: retorna `1.0`.
- Si la primera variable ya esta en evidencia:
  - multiplica su probabilidad local por la recursion del resto.
- Si no esta en evidencia:
  - suma las dos ramas (`True` y `False`) ponderadas por probabilidad local.

### 5.3 Funcion `normalize(distribution)`

Convierte valores no normalizados a distribucion valida:

`P_i = value_i / sum(values)`

Si la suma es `0.0`, lanza `ValueError` para evitar division invalida.

---

## 6. Interfaz de consola y validacion (`main.py` + `utils.py`)

### 6.1 Mejoras implementadas en validacion de entrada

En esta fase se reforzo el flujo de usuario:

- Seleccion de consulta con reintento hasta dato valido.
- Opcion `0` para volver sin ejecutar consulta.
- Lectura de evidencia con validacion estricta por variable.
- Mensajes explicitos para entradas invalidas.

### 6.2 Convenciones de parseo (`utils.py`)

Entradas verdaderas:

- `s`, `si`, `y`, `yes`, `true`, `1`

Entradas falsas:

- `n`, `no`, `false`, `0`

Entradas desconocidas:

- `d`, `desconocido`, ``, `?`

La funcion `is_valid_yes_no_unknown_input` permite diferenciar valor desconocido de texto invalido.

---

## 7. Escenarios de prueba (`scenarios.py`)

La constante `SCENARIOS` define una lista de casos con:

- `name`
- `query`
- `evidence`
- `description`

`run_all_scenarios(network)` ejecuta cada caso y muestra resultados.

Resultados observados en validacion actual:

- `P(BackendSaturado=si | Error500, ServicioNoDisponible, LatenciaAlta) = 0.5801`
- `P(GatewayCaido=si | ServicioNoDisponible, LatenciaAlta, no Error500) = 0.7320`

---

## 8. Complejidad y rendimiento

El algoritmo por enumeracion exacta recorre combinaciones de variables ocultas.

- Complejidad aproximada: exponencial en el numero de variables no observadas.
- Ventaja: implementacion clara, fiel al capitulo 13 y suficiente para redes pequenas (8-12 nodos).

---

## 9. Como extender el sistema

### 9.1 Agregar un nodo nuevo

1. Definir nombre, padres y CPT en `model.py`.
2. Asegurar que padres ya existan antes de insertar el nodo.
3. Verificar filas CPT (`2^n`).
4. Ejecutar programa y validar con opcion `3`.

### 9.2 Agregar un escenario

1. Crear un nuevo diccionario en `SCENARIOS`.
2. Definir `query` y `evidence` coherentes con la red.
3. Ejecutar opcion `2` para validar.

### 9.3 Ajustar probabilidades

1. Editar CPT en `model.py`.
2. Re-ejecutar escenarios.
3. Documentar impacto en resultados para trazabilidad.

---

## 10. Validacion tecnica realizada

Comandos ejecutados:

```bash
python3 -m py_compile main.py node.py bayesian_network.py inference.py model.py scenarios.py utils.py
python3 main.py
```

Estado:

- Compilacion: exitosa
- Ejecucion: exitosa
- Escenarios: ejecutan sin errores
- Manejo de entradas invalidas: validado

Comentario:
Con estas pruebas dejamos una base estable para integrar despues los ajustes finales de los demas integrantes.

---

## 11. Limitaciones conocidas

- No hay aprendizaje automatico de CPT desde datos reales.
- No existe interfaz grafica (solo consola).
- No hay persistencia de consultas/evidencias en archivo.
- No hay medicion automatica de tiempos por escenario.

Estas limitaciones son aceptables para el alcance academico del proyecto.
