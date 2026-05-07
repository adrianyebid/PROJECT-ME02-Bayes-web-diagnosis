from __future__ import annotations

from inference import enumeration_ask
from utils import print_distribution, print_evidence


SCENARIOS = [
    {
        "name": "Posible caida de base de datos",
        "query": "BaseDatosCaida",
        "evidence": {
            "Error500": True,
            "LatenciaAlta": True,
            "LoginFallido": False,
        },
        "description": "Evalua si la base de datos caida se vuelve mas probable ante error 500 y latencia alta.",
    },
    {
        "name": "Backend saturado",
        "query": "BackendSaturado",
        "evidence": {
            "Error500": True,
            "ServicioNoDisponible": True,
            "LatenciaAlta": True,
        },
        "description": "Estimacion de saturacion de backend dada evidencia de errores y caida del servicio.",
    },
    {
        "name": "Problema de autenticacion",
        "query": "ErrorAutenticacion",
        "evidence": {
            "LoginFallido": True,
            "Error500": False,
            "LatenciaAlta": False,
        },
        "description": "Valora si existe un error de autenticacion cuando falla el login.",
    },
    {
        "name": "Problema de red o conexion",
        "query": "ConexionInestable",
        "evidence": {
            "LatenciaAlta": True,
            "Error500": False,
            "ServicioNoDisponible": False,
        },
        "description": "Evalua si la conexion inestable explica la latencia observada.",
    },
    {
        "name": "Caida del gateway",
        "query": "GatewayCaido",
        "evidence": {
            "ServicioNoDisponible": True,
            "LatenciaAlta": True,
            "Error500": False,
        },
        "description": "Evalua la probabilidad de caida del gateway ante indisponibilidad y latencia.",
    },
]


def run_all_scenarios(network) -> None:
    print("\n=== Escenarios de prueba ===")
    for index, scenario in enumerate(SCENARIOS, start=1):
        print(f"\n[{index}] {scenario['name']}")
        print(f"Descripcion: {scenario['description']}")
        print_evidence(scenario["evidence"])
        print(f"Consulta: {scenario['query']}")
        distribution = enumeration_ask(
            scenario["query"], scenario["evidence"], network
        )
        print_distribution(scenario["query"], distribution)
