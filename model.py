
"""
Módulo responsable de la construcción y configuración del modelo probabilístico
del sistema BayesWebDiagnosis.

Este archivo define la red bayesiana completa para el diagnóstico de fallas en
una aplicación web distribuida. Incluye:
  - La definición de todos los nodos causa y nodos síntoma.
  - Las tablas de probabilidad condicional (CPT) de cada nodo.
  - La función que construye y retorna la red bayesiana lista para ser usada
    por el motor de inferencia.

Responsable: Integrante 3 — Diseño de la red bayesiana y tablas CPT.

"""

from __future__ import annotations

from bayesian_network import BayesianNetwork
from node import Node




# La red modela las relaciones causales entre los posibles fallos internos de
# una aplicación web distribuida (causas) y los síntomas observables por el
# sistema o el usuario (efectos).
#
# Estructura causal:
#
#   BaseDatosCaida ────┐
#                       ├──► Error500 ────┐
#   BackendSaturado ───┘                   ├──► UsuarioAfectado
#                                          │
#   GatewayCaido ──────┐                  │
#                       ├──► LatenciaAlta ┘
#   ConexionInestable ─┘
#
#   ErrorAutenticacion ──────────────────► LoginFallido
#
#   GatewayCaido ──────┐
#   BackendSaturado ───┼──────────────────► ServicioNoDisponible
#   BaseDatosCaida ───┘
#
# Tipos de nodo:
#   - Nodos causa (sin padres): representan fallas independientes del sistema.
#   - Nodos síntoma (con padres): representan manifestaciones observables.
#
# Todos los nodos son variables booleanas:
#   True  = la falla o síntoma está presente.
#   False = la falla o síntoma está ausente.
# =============================================================================


def create_web_diagnosis_network() -> BayesianNetwork:
    """
    Construye y retorna la red bayesiana completa del sistema de diagnóstico web.

    La red se construye añadiendo primero los nodos causa (sin padres) y luego
    los nodos síntoma (con padres), respetando el orden topológico requerido
    por el algoritmo de inferencia por enumeración.

    Returns:
        BayesianNetwork: Red bayesiana validada y lista para inferencia.

    Raises:
        ValueError: Si alguna CPT es incoherente o el orden topológico
                    es incorrecto.
    """
    network = BayesianNetwork()

    # =========================================================================
    # NODOS CAUSA — Variables independientes (sin padres)
    # =========================================================================
    # Estas variables representan fallas internas del sistema que ocurren
    # de forma autónoma. Sus probabilidades a priori se estiman en función
    # de datos históricos típicos de sistemas web en producción.
    # =========================================================================

    # P(BaseDatosCaida = True) = 0.05
    # Justificación: Las bases de datos son componentes robustos con alta
    # disponibilidad. Una tasa de falla del 5% refleja incidentes poco
    # frecuentes pero posibles (mantenimiento, corrupción, sobrecarga extrema).
    nodo_base_datos_caida = Node(
        name="BaseDatosCaida",
        parents=[],
        cpt={(): 0.05}
    )

    # P(BackendSaturado = True) = 0.10
    # Justificación: El backend es más susceptible a saturación por picos de
    # tráfico, bucles infinitos o fugas de memoria. Un 10% refleja que es
    # un evento más frecuente que una caída de base de datos.
    nodo_backend_saturado = Node(
        name="BackendSaturado",
        parents=[],
        cpt={(): 0.10}
    )

    # P(GatewayCaido = True) = 0.04
    # Justificación: El API Gateway es un componente crítico pero generalmente
    # estable y redundante. Su probabilidad de falla es la más baja entre los
    # nodos causa, reflejando alta disponibilidad del componente de entrada.
    nodo_gateway_caido = Node(
        name="GatewayCaido",
        parents=[],
        cpt={(): 0.04}
    )

    # P(ConexionInestable = True) = 0.12
    # Justificación: Los problemas de red son los más comunes en entornos
    # distribuidos. Un 12% refleja inestabilidades frecuentes en ISPs,
    # VPNs, o conexiones entre microservicios.
    nodo_conexion_inestable = Node(
        name="ConexionInestable",
        parents=[],
        cpt={(): 0.12}
    )

    # P(ErrorAutenticacion = True) = 0.08
    # Justificación: Fallos en el servicio de autenticación son moderadamente
    # comunes: pueden deberse a tokens expirados, problemas con el proveedor
    # de identidad o errores de configuración.
    nodo_error_autenticacion = Node(
        name="ErrorAutenticacion",
        parents=[],
        cpt={(): 0.08}
    )

    # =========================================================================
    # NODOS SÍNTOMA — Variables dependientes (con padres)
    # =========================================================================
    # Estas variables representan síntomas observables. Sus CPTs definen
    # P(Síntoma = True | combinación de valores de sus padres).
    #
    # Principio de diseño de las CPTs:
    #   - Si todos los padres están activos (True), la probabilidad del
    #     síntoma debe ser muy alta (efecto combinado).
    #   - Si ningún padre está activo (False, False, ...), la probabilidad
    #     del síntoma debe ser muy baja (ruido de fondo o causas externas
    #     no modeladas).
    #   - Valores intermedios reflejan la influencia parcial de cada causa.
    # =========================================================================

    # Nodo: Error500
    # Padres: BaseDatosCaida, BackendSaturado
    # Descripción: Un error HTTP 500 indica un fallo interno del servidor.
    # Es causado principalmente por una base de datos caída o un backend
    # saturado. La combinación de ambas causas eleva la probabilidad casi
    # a la certeza.
    #
    # Tabla CPT:
    #   BaseDatosCaida | BackendSaturado | P(Error500 = True)
    #   ─────────────────────────────────────────────────────
    #   True           | True            | 0.95  (doble causa activa)
    #   True           | False           | 0.85  (BD caída es causa fuerte)
    #   False          | True            | 0.70  (backend saturado también genera 500)
    #   False          | False           | 0.05  (ruido: otras causas no modeladas)
    nodo_error500 = Node(
        name="Error500",
        parents=["BaseDatosCaida", "BackendSaturado"],
        cpt={
            (True,  True):  0.95,
            (True,  False): 0.85,
            (False, True):  0.70,
            (False, False): 0.05,
        }
    )

    # Nodo: LatenciaAlta
    # Padres: GatewayCaido, ConexionInestable
    # Descripción: La latencia alta en las respuestas puede deberse a un
    # gateway caído (que retarda el enrutamiento) o a una conexión inestable
    # (que introduce pérdidas de paquetes y retransmisiones).
    #
    # Tabla CPT:
    #   GatewayCaido | ConexionInestable | P(LatenciaAlta = True)
    #   ──────────────────────────────────────────────────────────
    #   True         | True              | 0.90  (doble causa: latencia casi segura)
    #   True         | False             | 0.75  (gateway caído genera latencia alta)
    #   False        | True              | 0.65  (conexión inestable también la genera)
    #   False        | False             | 0.10  (tráfico elevado u otras causas menores)
    nodo_latencia_alta = Node(
        name="LatenciaAlta",
        parents=["GatewayCaido", "ConexionInestable"],
        cpt={
            (True,  True):  0.90,
            (True,  False): 0.75,
            (False, True):  0.65,
            (False, False): 0.10,
        }
    )

    # Nodo: LoginFallido
    # Padre: ErrorAutenticacion
    # Descripción: Un fallo de inicio de sesión es el síntoma más directo de
    # un error en el servicio de autenticación. También puede ocurrir por
    # contraseñas incorrectas del usuario (ruido de fondo bajo).
    #
    # Tabla CPT:
    #   ErrorAutenticacion | P(LoginFallido = True)
    #   ─────────────────────────────────────────────
    #   True               | 0.90  (fallo de autenticación → login casi siempre falla)
    #   False              | 0.08  (errores del usuario: contraseña incorrecta)
    nodo_login_fallido = Node(
        name="LoginFallido",
        parents=["ErrorAutenticacion"],
        cpt={
            (True,):  0.90,
            (False,): 0.08,
        }
    )

    # Nodo: ServicioNoDisponible
    # Padres: GatewayCaido, BackendSaturado, BaseDatosCaida
    # Descripción: El servicio aparece como no disponible cuando alguna capa
    # crítica de la arquitectura falla completamente. Tres componentes pueden
    # causar esto: el gateway (punto de entrada), el backend (procesamiento)
    # o la base de datos (persistencia).
    #
    # Tabla CPT (8 filas para 3 padres booleanos):
    #   Gateway | Backend | BD    | P(ServicioNoDisponible = True)
    #   ─────────────────────────────────────────────────────────
    #   True    | True    | True  | 0.98  (colapso total: certeza casi absoluta)
    #   True    | True    | False | 0.92  (gateway + backend caídos: muy probable)
    #   True    | False   | True  | 0.95  (gateway + BD: muy probable)
    #   True    | False   | False | 0.80  (solo gateway caído: probable)
    #   False   | True    | True  | 0.90  (backend + BD: probable)
    #   False   | True    | False | 0.65  (solo backend saturado: moderado)
    #   False   | False   | True  | 0.75  (solo BD caída: moderado-alto)
    #   False   | False   | False | 0.03  (ruido: otras causas externas)
    nodo_servicio_no_disponible = Node(
        name="ServicioNoDisponible",
        parents=["GatewayCaido", "BackendSaturado", "BaseDatosCaida"],
        cpt={
            (True,  True,  True):  0.98,
            (True,  True,  False): 0.92,
            (True,  False, True):  0.95,
            (True,  False, False): 0.80,
            (False, True,  True):  0.90,
            (False, True,  False): 0.65,
            (False, False, True):  0.75,
            (False, False, False): 0.03,
        }
    )

    # Nodo: UsuarioAfectado
    # Padres: Error500, LatenciaAlta
    # Descripción: Un usuario está afectado cuando experimenta errores directos
    # (Error500) o lentitud significativa (LatenciaAlta). Es el nodo de mayor
    # nivel en la jerarquía de síntomas, representando el impacto final.
    #
    # Tabla CPT:
    #   Error500 | LatenciaAlta | P(UsuarioAfectado = True)
    #   ────────────────────────────────────────────────────
    #   True     | True         | 0.95  (errores + lentitud: impacto total)
    #   True     | False        | 0.80  (solo errores: impacto alto)
    #   False    | True         | 0.60  (solo lentitud: impacto moderado)
    #   False    | False        | 0.05  (ruido: problemas del lado del cliente)
    nodo_usuario_afectado = Node(
        name="UsuarioAfectado",
        parents=["Error500", "LatenciaAlta"],
        cpt={
            (True,  True):  0.95,
            (True,  False): 0.80,
            (False, True):  0.60,
            (False, False): 0.05,
        }
    )

    # =========================================================================
    # CONSTRUCCIÓN DE LA RED
    # Los nodos se añaden en orden topológico: primero las causas (raíces),
    # luego los síntomas (hojas). Esto garantiza que cuando se agrega un nodo,
    # todos sus padres ya están en la red.
    # =========================================================================
    nodos_en_orden_topologico = [
        # --- Nivel 0: Nodos causa (sin padres) ---
        nodo_base_datos_caida,
        nodo_backend_saturado,
        nodo_gateway_caido,
        nodo_conexion_inestable,
        nodo_error_autenticacion,
        # --- Nivel 1: Nodos síntoma directos ---
        nodo_error500,
        nodo_latencia_alta,
        nodo_login_fallido,
        nodo_servicio_no_disponible,
        # --- Nivel 2: Nodo síntoma compuesto ---
        nodo_usuario_afectado,
    ]

    for nodo in nodos_en_orden_topologico:
        network.add_node(nodo)

    # Validación final: verifica integridad de la red (padres existentes y
    # orden topológico correcto). Lanza ValueError si detecta inconsistencias.
    network.validate_network()

    return network