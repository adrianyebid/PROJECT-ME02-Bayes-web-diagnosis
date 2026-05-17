from __future__ import annotations

from typing import Optional

from inference import enumeration_ask
from model import create_web_diagnosis_network
from scenarios import run_all_scenarios, run_all_scenarios_with_timing, run_full_analysis
from utils import (
    is_valid_yes_no_unknown_input,
    parse_yes_no_unknown,
    print_distribution,
)
from visualization import (
    generate_all_ascii_diagrams,
    generate_all_charts,
)


def print_header() -> None:
    print("=" * 45)
    print("BAYES WEB DIAGNOSIS")
    print("Sistema bayesiano de diagnostico web")
    print("=" * 45)


def select_query_variable(variables) -> Optional[str]:
    while True:
        selected = input(
            "\nNumero de variable de consulta (0 para volver): "
        ).strip()

        if selected == "0":
            return None

        if selected.isdigit() and 1 <= int(selected) <= len(variables):
            return variables[int(selected) - 1]

        print("Seleccion invalida. Debes ingresar un numero de la lista.")


def read_evidence_value(variable: str) -> Optional[bool]:
    while True:
        raw = input(f"{variable} [s/n/d]: ")
        if is_valid_yes_no_unknown_input(raw):
            return parse_yes_no_unknown(raw)
        print("Entrada invalida. Usa: s (si), n (no) o d (desconocido).")


def manual_query(network) -> None:
    variables = network.get_variables()
    print("\nVariables disponibles:")
    for index, name in enumerate(variables, start=1):
        print(f"{index}. {name}")

    query = select_query_variable(variables)
    if query is None:
        return

    evidence = {}
    print("\nIngresa evidencia (s = si, n = no, d = desconocido).")
    for variable in variables:
        if variable == query:
            continue
        value = read_evidence_value(variable)
        if value is None:
            continue
        evidence[variable] = value

    distribution = enumeration_ask(query, evidence, network)
    print_distribution(query, distribution)


def run_full_analysis_menu(network) -> None:
    print("\nEjecutando analisis completo (escenarios + sensibilidad)...")
    results = run_full_analysis(network)

    print("\nGenerando graficos...")
    prior_values = {}
    for scenario in results["escenarios_base"]:
        q = scenario["query"]
        if q not in prior_values:
            dist = enumeration_ask(q, {}, network)
            prior_values[q] = dist[True]

    generate_all_charts(
        results["escenarios_base"],
        results["analisis_sensibilidad"],
        prior_values,
    )

    print("\nGenerando diagramas de flujo...")
    generate_all_ascii_diagrams()


def run_diagrams_menu(network) -> None:
    generate_all_ascii_diagrams()


def run_menu() -> None:
    network = create_web_diagnosis_network()
    while True:
        print_header()
        print("1. Ejecutar consulta manual")
        print("2. Ejecutar escenarios de prueba")
        print("3. Mostrar estructura de la red")
        print("4. Ejecutar escenarios con medicion de tiempo")
        print("5. Analisis completo (sensibilidad + graficos)")
        print("6. Mostrar diagramas de flujo (ASCII)")
        print("7. Salir")
        option = input("\nSeleccione una opcion: ").strip()

        if option == "1":
            manual_query(network)
        elif option == "2":
            run_all_scenarios(network)
        elif option == "3":
            network.show_structure()
        elif option == "4":
            run_all_scenarios_with_timing(network)
        elif option == "5":
            run_full_analysis_menu(network)
        elif option == "6":
            run_diagrams_menu(network)
        elif option == "7":
            print("Saliendo...")
            break
        else:
            print("Opcion invalida.")

        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    run_menu()
