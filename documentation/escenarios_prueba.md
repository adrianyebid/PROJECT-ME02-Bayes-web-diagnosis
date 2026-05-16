# Escenarios de prueba

Este documento deja la base de escenarios para validar el comportamiento de la red bayesiana.

## Escenarios implementados en `scenarios.py`

1. **Posible caida de base de datos**
   - Consulta: `BaseDatosCaida`
   - Evidencia: `Error500=si`, `LatenciaAlta=si`, `LoginFallido=no`

2. **Backend saturado**
   - Consulta: `BackendSaturado`
   - Evidencia: `Error500=si`, `ServicioNoDisponible=si`, `LatenciaAlta=si`

3. **Problema de autenticacion**
   - Consulta: `ErrorAutenticacion`
   - Evidencia: `LoginFallido=si`, `Error500=no`, `LatenciaAlta=no`

4. **Problema de red o conexion**
   - Consulta: `ConexionInestable`
   - Evidencia: `LatenciaAlta=si`, `Error500=no`, `ServicioNoDisponible=no`

5. **Caida del gateway**
   - Consulta: `GatewayCaido`
   - Evidencia: `ServicioNoDisponible=si`, `LatenciaAlta=si`, `Error500=no`

## Resultados base de referencia

- `P(BaseDatosCaida=si | evidencia_1) = 0.2824`
- `P(BackendSaturado=si | evidencia_2) = 0.5801`
- `P(ErrorAutenticacion=si | evidencia_3) = 0.4945`
- `P(ConexionInestable=si | evidencia_4) = 0.4573`
- `P(GatewayCaido=si | evidencia_5) = 0.7320`

## Criterio de verificacion

Para cada escenario:

- `P(variable=si | evidencia) + P(variable=no | evidencia) = 1.0`
- La ejecucion no debe lanzar errores.

## Pendiente para el integrante 6

- Agregar analisis e interpretacion detallada de cada resultado.
- Comparar resultados al ajustar CPT en nuevas iteraciones.
- (Opcional) Medir tiempo de ejecucion por escenario.
