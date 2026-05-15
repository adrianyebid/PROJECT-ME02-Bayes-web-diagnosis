# Validacion final de ejecucion

Fecha de validacion: 2026-05-15
Responsable: Integrante 7

## 1. Objetivo

Comprobar que el proyecto:

- Compila sin errores.
- Ejecuta desde cero.
- Responde consultas manuales.
- Ejecuta escenarios de prueba.
- Maneja entradas invalidas sin fallar.

---

## 2. Pruebas ejecutadas

### 2.1 Compilacion de modulos

Comando:

```bash
python3 -m py_compile main.py node.py bayesian_network.py inference.py model.py scenarios.py utils.py
```

Resultado:

- Exitoso (sin errores de sintaxis).

### 2.2 Ejecucion de escenarios predefinidos

Comando usado (modo script):

```bash
python3 - <<'PY'
from model import create_web_diagnosis_network
from scenarios import run_all_scenarios

network = create_web_diagnosis_network()
run_all_scenarios(network)
PY
```

Resultado:

- Los 5 escenarios se ejecutan correctamente.
- Se imprimen distribuciones para cada consulta.

Valores destacados observados:

- `P(BaseDatosCaida=si | Error500, LatenciaAlta, no LoginFallido) = 0.2824`
- `P(BackendSaturado=si | Error500, ServicioNoDisponible, LatenciaAlta) = 0.5801`
- `P(GatewayCaido=si | ServicioNoDisponible, LatenciaAlta, no Error500) = 0.7320`

### 2.3 Prueba de validacion de entrada invalida

Caso probado:

- Ingreso de valor invalido (`x`) en captura de evidencia.

Resultado:

- El sistema no falla.
- Muestra mensaje: "Entrada invalida. Usa: s (si), n (no) o d (desconocido)."
- Solicita nuevamente el valor correcto.

### 2.4 Prueba de salida limpia

Caso probado:

- Salida por opcion `4` desde menu principal.

Resultado:

- Cierre controlado de aplicacion sin excepciones.

---

## 3. Conclusiones de validacion

- El proyecto se ejecuta correctamente con Python estandar.
- La inferencia responde para consultas manuales y escenarios.
- El manejo de errores de entrada mejora robustez de demostracion.
- El estado actual es apto para entrega academica y exposicion.

---

## 4. Recomendacion previa a entrega

Antes de presentar:

1. Ejecutar `python3 main.py` en el equipo de exposicion.
2. Hacer una corrida rapida de opcion `2` (escenarios).
3. Mostrar una consulta manual breve en opcion `1`.
4. Tener abiertos `manual_usuario.md` y `manual_tecnico.md` para responder preguntas.
