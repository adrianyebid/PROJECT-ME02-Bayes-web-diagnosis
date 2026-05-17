from __future__ import annotations

import json
import time
from typing import Any, Dict, List

from inference import enumeration_ask
from utils import (
    bool_to_spanish,
    format_probability,
    print_distribution,
    print_evidence,
)

SCENARIOS: List[Dict[str, Any]] = [
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

ALL_VARIABLES = [
    "BaseDatosCaida",
    "BackendSaturado",
    "GatewayCaido",
    "ConexionInestable",
    "ErrorAutenticacion",
    "Error500",
    "LatenciaAlta",
    "LoginFallido",
    "ServicioNoDisponible",
    "UsuarioAfectado",
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


def run_all_scenarios_with_timing(network) -> List[Dict[str, Any]]:
    results = []
    print("\n=== Escenarios de prueba (con medicion de tiempo) ===")
    for index, scenario in enumerate(SCENARIOS, start=1):
        print(f"\n[{index}] {scenario['name']}")
        print(f"Descripcion: {scenario['description']}")
        print_evidence(scenario["evidence"])
        print(f"Consulta: {scenario['query']}")

        start = time.perf_counter()
        distribution = enumeration_ask(
            scenario["query"], scenario["evidence"], network
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        print_distribution(scenario["query"], distribution)
        print(f"Tiempo de ejecucion: {elapsed_ms:.4f} ms")

        results.append({
            "name": scenario["name"],
            "query": scenario["query"],
            "evidence": {
                k: bool_to_spanish(v) for k, v in scenario["evidence"].items()
            },
            "p_true": round(distribution[True], 6),
            "p_false": round(distribution[False], 6),
            "time_ms": round(elapsed_ms, 4),
        })
    return results


def generate_sensitivity_variations(
    scenario: Dict[str, Any],
) -> List[Dict[str, Any]]:
    query = scenario["query"]
    base_evidence = dict(scenario["evidence"])
    variations = []

    variations.append({
        "label": "Caso base (evidencia definida)",
        "query": query,
        "evidence": dict(base_evidence),
    })

    variations.append({
        "label": "Sin evidencia (probabilidad a priori)",
        "query": query,
        "evidence": {},
    })

    for var in base_evidence:
        reduced = dict(base_evidence)
        del reduced[var]
        variations.append({
            "label": f"Sin observar '{var}'",
            "query": query,
            "evidence": reduced,
        })

    for var, original_value in base_evidence.items():
        toggled = dict(base_evidence)
        toggled[var] = not original_value
        variations.append({
            "label": f"'{var}' = {bool_to_spanish(not original_value)} (invertido)",
            "query": query,
            "evidence": toggled,
        })

    all_symptoms_true = {}
    for var in ALL_VARIABLES:
        if var != query:
            all_symptoms_true[var] = True
    variations.append({
        "label": "Todos los sintomas presentes",
        "query": query,
        "evidence": all_symptoms_true,
    })

    all_symptoms_false = {}
    for var in ALL_VARIABLES:
        if var != query:
            all_symptoms_false[var] = False
    variations.append({
        "label": "Ningun sintoma presente",
        "query": query,
        "evidence": all_symptoms_false,
    })

    return variations


def run_sensitivity_analysis(network) -> List[Dict[str, Any]]:
    all_results = []
    print("\n=== Analisis de sensibilidad ===")
    print("(Variando evidencia para cada escenario)\n")

    for scenario_index, scenario in enumerate(SCENARIOS, start=1):
        print(f"\n{'=' * 55}")
        print(f"Escenario {scenario_index}: {scenario['name']}")
        print(f"Consulta: {scenario['query']}")
        print(f"{'=' * 55}")

        variations = generate_sensitivity_variations(scenario)
        scenario_results = {
            "scenario": scenario["name"],
            "query": scenario["query"],
            "variations": [],
        }

        for var_index, variation in enumerate(variations, start=1):
            label = variation["label"]
            evidence = variation["evidence"]

            print(f"\n  [{var_index}] {label}")
            if evidence:
                print(f"      Evidencia: {', '.join(f'{k}={bool_to_spanish(v)}' for k, v in evidence.items())}")
            else:
                print(f"      Evidencia: (sin evidencia)")
            print(f"      Consulta: {variation['query']}")

            start = time.perf_counter()
            distribution = enumeration_ask(
                variation["query"], evidence, network
            )
            elapsed_ms = (time.perf_counter() - start) * 1000

            print(f"      P({variation['query']}=si | evidencia) = {format_probability(distribution[True])}")
            print(f"      P({variation['query']}=no | evidencia) = {format_probability(distribution[False])}")
            print(f"      Tiempo: {elapsed_ms:.4f} ms")

            scenario_results["variations"].append({
                "label": label,
                "evidence": {
                    k: bool_to_spanish(v) for k, v in evidence.items()
                },
                "p_true": round(distribution[True], 6),
                "p_false": round(distribution[False], 6),
                "time_ms": round(elapsed_ms, 4),
            })

        all_results.append(scenario_results)

    return all_results


def compare_prior_vs_posterior(network) -> None:
    print("\n=== Comparacion: Probabilidad a priori vs a posteriori ===")
    print(f"{'Variable':<25} {'P(si) a priori':<15} {'P(si) escenario':<18} {'Cambio':<10}")
    print("-" * 68)

    for scenario in SCENARIOS:
        query = scenario["query"]

        prior_dist = enumeration_ask(query, {}, network)
        prior_p = prior_dist[True]

        posterior_dist = enumeration_ask(query, scenario["evidence"], network)
        posterior_p = posterior_dist[True]

        change = posterior_p - prior_p
        direction = "sube" if change > 0 else "baja"
        print(
            f"{query:<25} {format_probability(prior_p):<15} "
            f"{format_probability(posterior_p):<18} "
            f"{direction} {abs(change):.4f}"
        )


def export_results_to_json(
    scenario_results: List[Dict[str, Any]],
    sensitivity_results: List[Dict[str, Any]],
    filepath: str = "resultados_escenarios.json",
) -> None:
    output = {
        "escenarios_base": scenario_results,
        "analisis_sensibilidad": sensitivity_results,
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nResultados exportados a '{filepath}'.")


def run_full_analysis(network) -> Dict[str, Any]:
    print("\n" + "=" * 55)
    print("ANALISIS COMPLETO DE ESCENARIOS DE PRUEBA")
    print("=" * 55)

    print("\n[FASE 1] Ejecucion de escenarios base con medicion de tiempo...")
    scenario_results = run_all_scenarios_with_timing(network)

    print("\n[FASE 2] Comparacion probabilidad a priori vs a posteriori...")
    compare_prior_vs_posterior(network)

    print("\n[FASE 3] Analisis de sensibilidad (variaciones de evidencia)...")
    sensitivity_results = run_sensitivity_analysis(network)

    print("\n[FASE 4] Exportando resultados a JSON...")
    export_results_to_json(scenario_results, sensitivity_results)

    print("\n=== Analisis completo finalizado ===")
    return {
        "escenarios_base": scenario_results,
        "analisis_sensibilidad": sensitivity_results,
    }
