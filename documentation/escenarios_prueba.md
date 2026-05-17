# Escenarios de prueba

Documento elaborado por el Integrante 6. Contiene la definicion, ejecucion y analisis detallado de los escenarios de prueba del sistema bayesiano de diagnostico web.

---

## 1. Escenarios implementados en `scenarios.py`

### Escenario 1: Posible caida de base de datos

| Campo | Valor |
|-------|-------|
| **Consulta** | `BaseDatosCaida` |
| **Evidencia** | `Error500=si`, `LatenciaAlta=si`, `LoginFallido=no` |
| **Descripcion** | Evalua si la base de datos caida se vuelve mas probable ante error 500 y latencia alta sin fallos de login. |

**Resultado base:**

```
P(BaseDatosCaida=si | evidencia) = 0.2824 (28.24%)
P(BaseDatosCaida=no | evidencia) = 0.7176 (71.76%)
```

**Analisis de sensibilidad (variaciones de evidencia):**

| # | Variacion | P(si) |
|---|-----------|-------|
| 1 | Caso base: Error500=si, LatenciaAlta=si, LoginFallido=no | 0.2824 |
| 2 | Sin evidencia (probabilidad a priori) | 0.0500 |
| 3 | Sin observar Error500: LatenciaAlta=si, LoginFallido=no | 0.0500 |
| 4 | Sin observar LatenciaAlta: Error500=si, LoginFallido=no | 0.2824 |
| 5 | Sin observar LoginFallido: Error500=si, LatenciaAlta=si | 0.2824 |
| 6 | Error500=no (invertido): Error500=no, LatenciaAlta=si, LoginFallido=no | 0.0083 |
| 7 | LatenciaAlta=no (invertido): Error500=si, LatenciaAlta=no, LoginFallido=no | 0.2824 |
| 8 | LoginFallido=si (invertido): Error500=si, LatenciaAlta=si, LoginFallido=si | 0.2824 |
| 9 | Todos los sintomas presentes (9 variables = si) | 0.0707 |
| 10 | Ningun sintoma presente (9 variables = no) | 0.0021 |

**Interpretacion:**

La probabilidad a priori de `BaseDatosCaida` es 0.05. Al observar los tres sintomas, sube a 0.2824 (+0.2324): mas de 5 veces mas probable.

El analisis revela que `Error500` es la UNICA variable determinante para esta consulta:
- Sin `Error500` (variacion 3), P vuelve exactamente a 0.0500 (la a priori). Esto es independencia condicional pura: sin observar `Error500`, `LatenciaAlta` y `LoginFallido` no afectan a `BaseDatosCaida`. En la red, `BaseDatosCaida` solo se conecta al resto a traves de `Error500` y `ServicioNoDisponible`; sin observar esos nodos, el camino esta bloqueado.
- Al invertir `Error500` a `no` (variacion 6), P se desploma a 0.0083, haciendo la hipotesis extremadamente improbable.
- `LatenciaAlta` y `LoginFallido` NO afectan a `BaseDatosCaida`: sus variaciones (7, 8) mantienen P=0.2824. Esto es correcto porque no son padres ni hijos de `BaseDatosCaida`, y los caminos indirectos pasan por v-structures bloqueadas.

Con todos los sintomas presentes (variacion 9), P=0.0707: otras causas como `BackendSaturado` compiten mejor. Con ningun sintoma (variacion 10), P=0.0021, practicamente descartada.

**Conclusion:** La presencia de `Error500=si` es el principal (y practicamente unico) indicio de `BaseDatosCaida`. Sin el, los otros sintomas no afectan esta hipotesis. Con `Error500=si`, la probabilidad sube al 28%, pero `BackendSaturado` es mas probable.

---

### Escenario 2: Backend saturado

| Campo | Valor |
|-------|-------|
| **Consulta** | `BackendSaturado` |
| **Evidencia** | `Error500=si`, `ServicioNoDisponible=si`, `LatenciaAlta=si` |
| **Descripcion** | Estimacion de saturacion de backend dada evidencia de errores, caida del servicio y latencia. |

**Resultado base:**

```
P(BackendSaturado=si | evidencia) = 0.5801 (58.01%)
P(BackendSaturado=no | evidencia) = 0.4199 (41.99%)
```

**Analisis de sensibilidad (variaciones de evidencia):**

| # | Variacion | P(si) |
|---|-----------|-------|
| 1 | Caso base: Error500=si, ServicioNoDisponible=si, LatenciaAlta=si | 0.5801 |
| 2 | Sin evidencia (probabilidad a priori) | 0.1000 |
| 3 | Sin observar Error500: ServicioNoDisponible=si, LatenciaAlta=si | 0.2964 |
| 4 | Sin observar ServicioNoDisponible: Error500=si, LatenciaAlta=si | 0.4680 |
| 5 | Sin observar LatenciaAlta: Error500=si, ServicioNoDisponible=si | 0.6042 |
| 6 | Error500=no (invertido): Error500=no, ServicioNoDisponible=si, LatenciaAlta=si | 0.1327 |
| 7 | ServicioNoDisponible=no (invertido): Error500=si, ServicioNoDisponible=no, LatenciaAlta=si | 0.3185 |
| 8 | LatenciaAlta=no (invertido): Error500=si, ServicioNoDisponible=si, LatenciaAlta=no | 0.6105 |
| 9 | Todos los sintomas presentes (9 variables = si) | 0.1136 |
| 10 | Ningun sintoma presente (9 variables = no) | 0.0125 |

**Interpretacion:**

Es uno de los escenarios mas concluyentes: P pasa de 0.10 a 0.5801, superando el 50% y siendo mas probable que la hipotesis alternativa.

`Error500` es la variable mas influyente: sin ella (variacion 3), P baja a 0.2964; al invertirla (variacion 6), P cae a 0.1327. Esto es coherente: `BackendSaturado` es padre directo de `Error500`.

`ServicioNoDisponible` tambien es importante (tambien es hijo de `BackendSaturado`): sin ella (variacion 4), P=0.4680; al invertirla (variacion 7), P=0.3185.

`LatenciaAlta` tiene un efecto contra-intuitivo: al removerla (variacion 5), P sube a 0.6042; al invertirla (variacion 8), P sube a 0.6105. Esto es "explaining away": con `LatenciaAlta=no`, el modelo descarta `GatewayCaido` y `ConexionInestable` como causas, concentrando la probabilidad en `BackendSaturado`.

Con todos los sintomas (variacion 9), P=0.1136: muchas causas compiten. Con ningun sintoma (variacion 10), P=0.0125: practicamente descartada.

**Conclusion:** `Error500=si` + `ServicioNoDisponible=si` + `LatenciaAlta=si` apuntan fuertemente a saturacion del backend (58.01%). Se recomienda verificar carga, CPU y colas de solicitudes del backend.

---

### Escenario 3: Problema de autenticacion

| Campo | Valor |
|-------|-------|
| **Consulta** | `ErrorAutenticacion` |
| **Evidencia** | `LoginFallido=si`, `Error500=no`, `LatenciaAlta=no` |
| **Descripcion** | Valora si existe un error de autenticacion cuando falla el login sin otros sintomas. |

**Resultado base:**

```
P(ErrorAutenticacion=si | evidencia) = 0.4945 (49.45%)
P(ErrorAutenticacion=no | evidencia) = 0.5055 (50.55%)
```

**Analisis de sensibilidad (variaciones de evidencia):**

| # | Variacion | P(si) |
|---|-----------|-------|
| 1 | Caso base: LoginFallido=si, Error500=no, LatenciaAlta=no | 0.4945 |
| 2 | Sin evidencia (probabilidad a priori) | 0.0800 |
| 3 | Sin observar LoginFallido: Error500=no, LatenciaAlta=no | 0.0800 |
| 4 | Sin observar Error500: LoginFallido=si, LatenciaAlta=no | 0.4945 |
| 5 | Sin observar LatenciaAlta: LoginFallido=si, Error500=no | 0.4945 |
| 6 | LoginFallido=no (invertido): LoginFallido=no, Error500=no, LatenciaAlta=no | 0.0094 |
| 7 | Error500=si (invertido): LoginFallido=si, Error500=si, LatenciaAlta=no | 0.4945 |
| 8 | LatenciaAlta=si (invertido): LoginFallido=si, Error500=no, LatenciaAlta=si | 0.4945 |
| 9 | Todos los sintomas presentes (9 variables = si) | 0.4945 |
| 10 | Ningun sintoma presente (9 variables = no) | 0.0094 |

**Interpretacion:**

`ErrorAutenticacion` es el unico padre de `LoginFallido` con P(LoginFallido=si | ErrorAutenticacion=si) = 0.90. Esta estructura hace que `LoginFallido` sea el unico sintoma relevante para esta consulta.

Sin evidencia, P=0.08. Al observar `LoginFallido=si`, P sube a 0.4945. El resultado es un empate tecnico: ~49.5% vs ~50.5%, reflejando que aunque `LoginFallido=si` es un indicio fuerte, existe un 8% de falsos positivos (login fallido sin error de autenticacion).

`Error500` y `LatenciaAlta` NO afectan esta consulta en absoluto (variaciones 4, 5, 7, 8 mantienen P=0.4945), demostrando independencia condicional: `ErrorAutenticacion` esta desconectada del resto de la red excepto a traves de `LoginFallido`.

La unica variable relevante es `LoginFallido`:
- Sin ella (variacion 3), P vuelve a la a priori 0.0800.
- Al invertirla a `no` (variacion 6), P se desploma a 0.0094, practicamente descartando el error de autenticacion.

Notablemente, "todos los sintomas presentes" (variacion 9) mantiene P=0.4945: los sintomas adicionales no ayudan ni perjudican la hipotesis de error de autenticacion, porque son condicionalmente independientes. Solo "ningun sintoma" (variacion 10) la descarta (P=0.0094) porque incluye `LoginFallido=no`.

**Conclusion:** Un `LoginFallido=si` aislado sugiere error de autenticacion pero no de forma concluyente (~49.5%). Para mayor certeza se necesitarian variables adicionales especificas del dominio de autenticacion (ej: codigo de error HTTP 401 vs 403).

---

### Escenario 4: Problema de red o conexion

| Campo | Valor |
|-------|-------|
| **Consulta** | `ConexionInestable` |
| **Evidencia** | `LatenciaAlta=si`, `Error500=no`, `ServicioNoDisponible=no` |
| **Descripcion** | Evalua si la conexion inestable explica la latencia observada cuando no hay otros sintomas. |

**Resultado base:**

```
P(ConexionInestable=si | evidencia) = 0.4573 (45.73%)
P(ConexionInestable=no | evidencia) = 0.5427 (54.27%)
```

**Analisis de sensibilidad (variaciones de evidencia):**

| # | Variacion | P(si) |
|---|-----------|-------|
| 1 | Caso base: LatenciaAlta=si, Error500=no, ServicioNoDisponible=no | 0.4573 |
| 2 | Sin evidencia (probabilidad a priori) | 0.1200 |
| 3 | Sin observar LatenciaAlta: Error500=no, ServicioNoDisponible=no | 0.1200 |
| 4 | Sin observar Error500: LatenciaAlta=si, ServicioNoDisponible=no | 0.4572 |
| 5 | Sin observar ServicioNoDisponible: LatenciaAlta=si, Error500=no | 0.4167 |
| 6 | LatenciaAlta=no (invertido): LatenciaAlta=no, Error500=no, ServicioNoDisponible=no | 0.0504 |
| 7 | Error500=si (invertido): LatenciaAlta=si, Error500=si, ServicioNoDisponible=no | 0.4569 |
| 8 | ServicioNoDisponible=si (invertido): LatenciaAlta=si, Error500=no, ServicioNoDisponible=si | 0.2289 |
| 9 | Todos los sintomas presentes (9 variables = si) | 0.1406 |
| 10 | Ningun sintoma presente (9 variables = no) | 0.0504 |

**Interpretacion:**

`ConexionInestable` comparte con `GatewayCaido` la paternidad de `LatenciaAlta`. Pasa de P=0.12 (a priori) a P=0.4573 con la evidencia, un aumento de +0.3373 pero sin superar el 50%.

`LatenciaAlta` es la variable mas influyente:
- Sin ella (variacion 3), P vuelve exactamente a la a priori 0.1200. `Error500` y `ServicioNoDisponible` no afectan a `ConexionInestable` porque no hay camino activo en la red cuando `LatenciaAlta` no se observa.
- Al invertirla a `no` (variacion 6), P cae a 0.0504.

`ServicioNoDisponible` tiene un impacto significativo:
- Sin el (variacion 5), P sube a 0.4167.
- Al invertirlo a `si` (variacion 8), P cae a 0.2289, porque `ServicioNoDisponible=si` apunta mas a `GatewayCaido` o `BackendSaturado` (que son sus padres directos).

`Error500` practicamente no afecta (variacion 7: P=0.4569, casi identico al caso base), porque no esta conectado causalmente a `ConexionInestable`; la leve diferencia se debe a efectos indirectos a traves de `UsuarioAfectado` y otras variables.

Con todos los sintomas (variacion 9), P=0.1406: `ConexionInestable` no explica bien una constelacion amplia de fallas. Con ningun sintoma (variacion 10), P=0.0504 (bajo, por debajo incluso de la a priori 0.12, porque la evidencia de sintomas negativos descarta causas en general).

**Conclusion:** Ante `LatenciaAlta=si` sin `Error500` ni `ServicioNoDisponible`, `ConexionInestable` es plausible (45.73%) pero no dominante. `GatewayCaido` es la alternativa principal. Se recomienda verificar metricas de red: paquetes perdidos, latencia de red, ancho de banda.

---

### Escenario 5: Caida del gateway

| Campo | Valor |
|-------|-------|
| **Consulta** | `GatewayCaido` |
| **Evidencia** | `ServicioNoDisponible=si`, `LatenciaAlta=si`, `Error500=no` |
| **Descripcion** | Evalua la probabilidad de caida del gateway ante indisponibilidad del servicio y latencia sin error 500. |

**Resultado base:**

```
P(GatewayCaido=si | evidencia) = 0.7320 (73.20%)
P(GatewayCaido=no | evidencia) = 0.2680 (26.80%)
```

**Analisis de sensibilidad (variaciones de evidencia):**

| # | Variacion | P(si) |
|---|-----------|-------|
| 1 | Caso base: ServicioNoDisponible=si, LatenciaAlta=si, Error500=no | 0.7320 |
| 2 | Sin evidencia (probabilidad a priori) | 0.0400 |
| 3 | Sin observar ServicioNoDisponible: LatenciaAlta=si, Error500=no | 0.1616 |
| 4 | Sin observar LatenciaAlta: ServicioNoDisponible=si, Error500=no | 0.3712 |
| 5 | Sin observar Error500: ServicioNoDisponible=si, LatenciaAlta=si | 0.5569 |
| 6 | ServicioNoDisponible=no (invertido): ServicioNoDisponible=no, LatenciaAlta=si, Error500=no | 0.0383 |
| 7 | LatenciaAlta=no (invertido): ServicioNoDisponible=si, LatenciaAlta=no, Error500=no | 0.1411 |
| 8 | Error500=si (invertido): ServicioNoDisponible=si, LatenciaAlta=si, Error500=si | 0.2534 |
| 9 | Todos los sintomas presentes (9 variables = si) | 0.0591 |
| 10 | Ningun sintoma presente (9 variables = no) | 0.0024 |

**Interpretacion:**

Este es el escenario con MAYOR certeza: `GatewayCaido` pasa de P=0.04 (a priori) a P=0.7320, un aumento masivo de +0.6920. La hipotesis es 18 veces mas probable que sin evidencia.

`GatewayCaido` es padre tanto de `ServicioNoDisponible` como de `LatenciaAlta`. Al observar ambos sintomas simultaneamente, la evidencia se refuerza de forma multiplicativa, produciendo la conclusion mas contundente del sistema.

`ServicioNoDisponible` es la variable mas critica:
- Sin ella (variacion 3), P cae drasticamente de 0.7320 a 0.1616 (-0.5704).
- Al invertirla a `no` (variacion 6), P se desploma a 0.0383, casi la a priori.

`LatenciaAlta` tambien es muy relevante:
- Sin ella (variacion 4), P baja a 0.3712 (-0.3608).
- Al invertirla a `no` (variacion 7), P cae a 0.1411.

`Error500=no` actua como filtro: sin esta observacion (variacion 5), P seria 0.5569. `Error500=no` descarta `BaseDatosCaida` y `BackendSaturado` como causas de `ServicioNoDisponible`, dejando a `GatewayCaido` como explicacion dominante (0.7320 vs 0.5569). Al invertir `Error500` a `si` (variacion 8), P baja a 0.2534 porque `BackendSaturado` y `BaseDatosCaida` ahora compiten como explicaciones alternativas de `ServicioNoDisponible`.

Con todos los sintomas (variacion 9), P=0.0591: muchas causas compiten. Con ningun sintoma (variacion 10), P=0.0024.

**Conclusion:** `ServicioNoDisponible=si` + `LatenciaAlta=si` + `Error500=no` es un perfil casi patognomonico de caida del gateway (73.20%). Es la conclusion mas solida del sistema. Se recomienda verificar inmediatamente el API Gateway: salud del servicio, balanceadores y conectividad con el backend.

---

## 2. Resumen comparativo de escenarios

| Escenario | Causa consultada | P(si) a priori | P(si \| evidencia) | Cambio | Conclusion |
|-----------|-----------------|----------------|-------------------|--------|------------|
| E1 | BaseDatosCaida | 0.0500 | 0.2824 | +0.2324 | Posible, no concluyente |
| E2 | BackendSaturado | 0.1000 | 0.5801 | +0.4801 | **Probable (58%)** |
| E3 | ErrorAutenticacion | 0.0800 | 0.4945 | +0.4145 | Ambiguo (~50%) |
| E4 | ConexionInestable | 0.1200 | 0.4573 | +0.3373 | Plausible, no dominante |
| E5 | GatewayCaido | 0.0400 | 0.7320 | +0.6920 | **Muy probable (73%)** |

---

## 3. Medicion de tiempos de ejecucion

Los tiempos de ejecucion varian segun la cantidad de variables ocultas en cada consulta (complejidad O(2^n) donde n = variables no observadas).

| Escenario | Variables ocultas | Tiempo aproximado (ms) |
|-----------|-------------------|------------------------|
| E1: BaseDatosCaida | 6 | ~4-8 ms |
| E2: BackendSaturado | 6 | ~4-8 ms |
| E3: ErrorAutenticacion | 6 | ~4-8 ms |
| E4: ConexionInestable | 6 | ~4-8 ms |
| E5: GatewayCaido | 6 | ~4-8 ms |

*Nota: Los tiempos exactos dependen del hardware. Con 10 variables y 3-4 observadas (6-7 ocultas), el algoritmo de enumeracion realiza aproximadamente 2^6 = 64 a 2^7 = 128 evaluaciones de la red.*

Para variaciones con 0 evidencia (9 variables ocultas), el tiempo sube a ~30-50 ms, y para variaciones con los 9 sintomas fijados (0 ocultas), el tiempo es <1 ms.

---

## 4. Verificacion de correctitud

Para todos los escenarios y sus variaciones se verifico:

- **Suma de probabilidades**: `P(si) + P(no) = 1.0` en todos los casos.
- **Sin errores de ejecucion**: todas las consultas se completan sin excepciones.
- **Coherencia semantica**: los resultados son consistentes con la estructura causal de la red.

---

## 5. Graficos generados

Los siguientes graficos se generan automaticamente al ejecutar la opcion "Analisis completo" del menu o mediante `visualization.py`:

| Archivo | Descripcion |
|---------|-------------|
| `graphs/comparacion_escenarios.png` | Barras comparativas de P(si) para los 5 escenarios base |
| `graphs/priori_vs_posteriori.png` | Comparacion de probabilidad a priori vs a posteriori |
| `graphs/tiempos_ejecucion.png` | Tiempos de ejecucion por escenario |
| `graphs/sensibilidad_completa.png` | Heatmap de sensibilidad con todos los escenarios |
| `graphs/sensibilidad_posible_caida_de_base_de_datos.png` | Barras de sensibilidad para escenario 1 |
| `graphs/sensibilidad_backend_saturado.png` | Barras de sensibilidad para escenario 2 |
| `graphs/sensibilidad_problema_de_autenticacion.png` | Barras de sensibilidad para escenario 3 |
| `graphs/sensibilidad_problema_de_red_o_conexion.png` | Barras de sensibilidad para escenario 4 |
| `graphs/sensibilidad_caida_del_gateway.png` | Barras de sensibilidad para escenario 5 |

---

## 6. Conclusiones generales

1. **El sistema funciona correctamente**: las probabilidades suman 1.0, los resultados son semanticamente coherentes con la estructura causal de la red, y los tiempos de ejecucion son aceptables para 10 nodos.

2. **La red bayesiana modela adecuadamente la incertidumbre**: en escenarios donde la evidencia es ambigua (E3, E4), el sistema refleja esa ambiguedad con probabilidades cercanas al 50%. En escenarios donde la evidencia es concluyente (E5), el sistema produce probabilidades altas (>70%).

3. **El analisis de sensibilidad es util**: permite entender que variables de evidencia tienen mayor impacto en cada consulta, lo cual ayuda a interpretar los resultados y a disenar estrategias de diagnostico (por ejemplo, que sintomas conviene verificar primero).

4. **La complejidad exponencial es manejable**: para 10 nodos, el algoritmo de enumeracion es perfectamente viable (<10 ms por consulta tipica). Para redes mas grandes, se podria implementar eliminacion de variables como optimizacion.
