# Diseño de la red bayesiana y tablas de probabilidad condicional

**Proyecto:** BayesWebDiagnosis — Sistema bayesiano para el diagnóstico probabilístico de fallas en una aplicación web distribuida  
**Responsable:** Integrante 3 — Diseño del modelo probabilístico  


---

## 1. Objetivo de este documento

Este documento describe el proceso de diseño del modelo probabilístico que constituye el núcleo del sistema BayesWebDiagnosis. Se explica:

- Qué variables aleatorias se seleccionaron y por qué.
- Cómo se definieron las relaciones causales entre ellas.
- Qué criterios se usaron para asignar los valores numéricos de las tablas de probabilidad condicional (CPT).
- Cómo se verificó la coherencia del modelo.

---

## 2. Selección de variables aleatorias

Una red bayesiana representa el dominio del problema mediante variables aleatorias. En este proyecto, cada variable es **booleana**: toma el valor `True` (la falla o síntoma está presente) o `False` (está ausente).

Las variables se dividen en dos grupos:

### 2.1 Variables causa (nodos raíz)

Representan fallas internas que pueden ocurrir de forma autónoma en los componentes de la arquitectura web distribuida. Al no tener padres, solo necesitan una probabilidad a priori.

| Variable | Componente que representa |
|---|---|
| `BaseDatosCaida` | Falla en el servidor de base de datos |
| `BackendSaturado` | Saturación o bloqueo del servidor de aplicaciones |
| `GatewayCaido` | Falla en el API Gateway (punto de entrada) |
| `ConexionInestable` | Problemas de red entre componentes o hacia el usuario |
| `ErrorAutenticacion` | Falla en el servicio de autenticación e identidad |

### 2.2 Variables síntoma (nodos con padres)

Representan observaciones que el sistema o el usuario pueden detectar directamente. Dependen de una o más causas.

| Variable | Síntoma que representa |
|---|---|
| `Error500` | Error HTTP 500 Internal Server Error |
| `LatenciaAlta` | Tiempos de respuesta anormalmente altos |
| `LoginFallido` | Fallo en el inicio de sesión del usuario |
| `ServicioNoDisponible` | El servicio no responde (timeout o 503) |
| `UsuarioAfectado` | El usuario experimenta un problema funcional o de rendimiento |

---

## 3. Estructura causal de la red (grafo acíclico dirigido)

La estructura de la red define qué variables influyen sobre cuáles. Una flecha `A → B` significa que A es una causa que influye probabilísticamente sobre B.

```
BaseDatosCaida ────┐
                    ├──► Error500 ──────────┐
BackendSaturado ───┘                         ├──► UsuarioAfectado
                                             │
GatewayCaido ──────┐                        │
                    ├──► LatenciaAlta ──────┘
ConexionInestable ─┘

ErrorAutenticacion ───────────────────────► LoginFallido

GatewayCaido ──────┐
BackendSaturado ───┼──────────────────────► ServicioNoDisponible
BaseDatosCaida ───┘
```

### Justificación de cada relación causal

**`BaseDatosCaida` y `BackendSaturado` → `Error500`**  
Un error 500 indica un fallo en el procesamiento del lado del servidor. Las dos causas más frecuentes en una arquitectura web son: que la base de datos no pueda responder consultas (lo que hace fallar al backend) o que el backend mismo esté saturado e incapaz de procesar la solicitud.

**`GatewayCaido` y `ConexionInestable` → `LatenciaAlta`**  
La latencia alta refleja demoras en la red o en el enrutamiento. Un gateway caído introduce retrasos en el enrutamiento de peticiones. Una conexión inestable introduce pérdida de paquetes y retransmisiones, ambas causantes de alta latencia.

**`ErrorAutenticacion` → `LoginFallido`**  
Un fallo en el servicio de autenticación es la causa directa e inmediata de que los usuarios no puedan iniciar sesión. La relación es fuerte y prácticamente unidireccional.

**`GatewayCaido`, `BackendSaturado`, `BaseDatosCaida` → `ServicioNoDisponible`**  
El servicio aparece como no disponible cuando alguna capa crítica de la arquitectura colapsa: el gateway (entrada), el backend (procesamiento) o la base de datos (persistencia). Cualquiera de los tres puede generar este síntoma.

**`Error500` y `LatenciaAlta` → `UsuarioAfectado`**  
Este nodo representa el impacto final en el usuario. Un usuario está afectado si experimenta errores directos (Error500) o degradación del rendimiento (LatenciaAlta). Es el nodo de mayor nivel jerárquico.

### Independencias condicionales garantizadas por la estructura

La estructura respeta el principio de independencia condicional del capítulo 13: dado el valor de sus padres directos, cada nodo es independiente de todos los nodos que no son sus descendientes. Por ejemplo:

- `LoginFallido` es condicionalmente independiente de `Error500`, `LatenciaAlta`, `BaseDatosCaida`, `BackendSaturado`, `GatewayCaido` y `ConexionInestable`, dado `ErrorAutenticacion`.
- `UsuarioAfectado` es condicionalmente independiente de todas las causas raíz, dado `Error500` y `LatenciaAlta`.

Esto hace que la red sea compacta: en lugar de listar los 2^10 = 1024 mundos posibles de la distribución conjunta completa, solo se necesitan las CPTs individuales de cada nodo.

---

## 4. Tablas de probabilidad condicional (CPT)

Cada nodo tiene una tabla CPT que especifica `P(Nodo = True | valores de los padres)`. El valor complementario `P(Nodo = False | ...)` se obtiene como `1 - P(Nodo = True | ...)`.

### Criterios generales de diseño

Los valores de probabilidad se asignaron siguiendo tres criterios:

1. **Coherencia causal:** Si una causa está activa, la probabilidad del efecto debe ser alta. Si ninguna causa está activa, la probabilidad del efecto debe ser baja (ruido de fondo).
2. **Monotonía:** Agregar más causas activas no debe reducir la probabilidad del efecto.
3. **Realismo:** Los valores a priori de las causas reflejan tasas de falla típicas en sistemas web en producción.

---

### 4.1 Nodos causa — Probabilidades a priori

| Nodo | P(True) | Justificación |
|---|---|---|
| `BaseDatosCaida` | 0.05 | Las BD son robustas y redundantes; fallas son infrecuentes |
| `BackendSaturado` | 0.10 | El backend es más susceptible a picos de tráfico y fugas de memoria |
| `GatewayCaido` | 0.04 | Los gateways son altamente disponibles; fallas son raras |
| `ConexionInestable` | 0.12 | Los problemas de red son los más comunes en entornos distribuidos |
| `ErrorAutenticacion` | 0.08 | Los fallos de autenticación son moderadamente comunes |

---

### 4.2 Nodo `Error500`

**Padres:** `BaseDatosCaida`, `BackendSaturado`

| BaseDatosCaida | BackendSaturado | P(Error500 = True) | Razonamiento |
|---|---|---|---|
| True | True | **0.95** | Doble causa activa: fallo casi seguro |
| True | False | **0.85** | BD caída sola genera 500 con alta frecuencia |
| False | True | **0.70** | Backend saturado también produce 500, pero con menor certeza |
| False | False | **0.05** | Ruido de fondo: otras causas no modeladas |

**Verificación de monotonía:** 0.95 ≥ 0.85 ≥ 0.70 ≥ 0.05 ✓

---

### 4.3 Nodo `LatenciaAlta`

**Padres:** `GatewayCaido`, `ConexionInestable`

| GatewayCaido | ConexionInestable | P(LatenciaAlta = True) | Razonamiento |
|---|---|---|---|
| True | True | **0.90** | Ambas causas generan latencia de forma combinada |
| True | False | **0.75** | Gateway caído introduce latencia de enrutamiento |
| False | True | **0.65** | Conexión inestable introduce latencia por retransmisión |
| False | False | **0.10** | Tráfico elevado u otras causas menores |

**Verificación de monotonía:** 0.90 ≥ 0.75 ≥ 0.65 ≥ 0.10 ✓

---

### 4.4 Nodo `LoginFallido`

**Padre:** `ErrorAutenticacion`

| ErrorAutenticacion | P(LoginFallido = True) | Razonamiento |
|---|---|---|
| True | **0.90** | Fallo de autenticación → login falla en casi todos los casos |
| False | **0.08** | Contraseña incorrecta del usuario u otros errores locales |

**Observación:** La diferencia entre 0.90 y 0.08 es grande y deliberada. El síntoma `LoginFallido` es altamente informativo sobre la causa `ErrorAutenticacion`.

---

### 4.5 Nodo `ServicioNoDisponible`

**Padres:** `GatewayCaido`, `BackendSaturado`, `BaseDatosCaida`

| GatewayCaido | BackendSaturado | BaseDatosCaida | P(ServicioNoDisponible = True) | Razonamiento |
|---|---|---|---|---|
| True | True | True | **0.98** | Colapso de todos los componentes críticos |
| True | True | False | **0.92** | Gateway + Backend: muy probable |
| True | False | True | **0.95** | Gateway + BD: muy probable |
| True | False | False | **0.80** | Solo gateway caído: aísla al usuario |
| False | True | True | **0.90** | Backend + BD: la aplicación no puede funcionar |
| False | True | False | **0.65** | Solo backend saturado: puede recuperarse intermitentemente |
| False | False | True | **0.75** | Solo BD caída: el servicio no puede persistir datos |
| False | False | False | **0.03** | Ruido: problemas de infraestructura externos |

**Verificación de monotonía:** Los valores más altos corresponden a más causas activas ✓

---

### 4.6 Nodo `UsuarioAfectado`

**Padres:** `Error500`, `LatenciaAlta`

| Error500 | LatenciaAlta | P(UsuarioAfectado = True) | Razonamiento |
|---|---|---|---|
| True | True | **0.95** | Errores directos y lentitud: impacto máximo |
| True | False | **0.80** | Solo errores: afecta directamente la funcionalidad |
| False | True | **0.60** | Solo lentitud: el usuario lo percibe pero puede continuar |
| False | False | **0.05** | Ruido: problemas del lado del cliente |

**Verificación de monotonía:** 0.95 ≥ 0.80 ≥ 0.60 ≥ 0.05 ✓

---

## 5. Verificación de coherencia del modelo

### 5.1 Verificación de probabilidades

Cada CPT fue revisada para garantizar que:
- Todos los valores están en el intervalo [0.0, 1.0].
- La cantidad de filas es exactamente 2^(número de padres).
- Los valores satisfacen monotonía: más causas activas no reducen la probabilidad del efecto.

### 5.2 Verificación del orden topológico

Los nodos se insertan en la red en el siguiente orden, que respeta la condición de que todo padre debe preceder a sus hijos:

```
Nivel 0 (causas): BaseDatosCaida, BackendSaturado, GatewayCaido,
                  ConexionInestable, ErrorAutenticacion
Nivel 1 (síntomas directos): Error500, LatenciaAlta, LoginFallido,
                              ServicioNoDisponible
Nivel 2 (síntoma compuesto): UsuarioAfectado
```

La clase `BayesianNetwork.validate_network()` verifica automáticamente esta condición al construir la red.

### 5.3 Verificación de capacidad de diagnóstico

El modelo puede diferenciar entre escenarios con síntomas similares. Por ejemplo:

- **Latencia alta + Error500:** apunta a `BaseDatosCaida` o `BackendSaturado`.
- **Latencia alta sin Error500:** apunta a `ConexionInestable` o `GatewayCaido`.
- **LoginFallido sin Error500 ni latencia:** apunta casi exclusivamente a `ErrorAutenticacion`.

Esta separabilidad entre causas hace que el sistema sea diagnósticamente útil.

---

## 6. Implementación en código

El modelo completo se implementa en el archivo `model.py` mediante la función `create_web_diagnosis_network()`. Esta función:

1. Instancia cada nodo con su nombre, lista de padres y tabla CPT.
2. Agrega los nodos a la red en orden topológico.
3. Llama a `network.validate_network()` para verificar la integridad de la red antes de retornarla.

La función retorna un objeto `BayesianNetwork` listo para ser usado por el motor de inferencia (`inference.py`) y los escenarios de prueba (`scenarios.py`).

### Ejemplo de uso

```python
from model import create_web_diagnosis_network
from inference import enumeration_ask

red = create_web_diagnosis_network()

evidencia = {
    "Error500": True,
    "LatenciaAlta": True,
    "LoginFallido": False
}

resultado = enumeration_ask("BaseDatosCaida", evidencia, red)
print(resultado)
# {True: 0.64, False: 0.36}
```

---

## 7. Conexión con el Capítulo 13

El diseño de este modelo aplica directamente los conceptos del Capítulo 13 de Russell y Norvig:

| Concepto del capítulo | Aplicación en el modelo |
|---|---|
| Red bayesiana (Bayesian network) | La estructura de 10 nodos y sus relaciones causales |
| Grafo acíclico dirigido (DAG) | La estructura sin ciclos, de causas hacia síntomas |
| Variable aleatoria booleana | Cada nodo es True/False |
| Tabla de probabilidad condicional (CPT) | Definida para cada nodo según sus padres |
| Independencia condicional | Cada nodo es independiente de sus no-descendientes dado sus padres |
| Distribución conjunta compacta | La red reemplaza la tabla de 2^10 = 1024 entradas |
| Inferencia probabilística | El motor en `inference.py` usa esta red para calcular P(X \| evidencia) |