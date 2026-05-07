from __future__ import annotations

from inference import enumeration_ask
from model import create_web_diagnosis_network
from scenarios import run_all_scenarios
from utils import parse_yes_no_unknown, print_distribution


def print_header() -> None:
    print("=" * 45)
    print("BAYES WEB DIAGNOSIS")
    print("Sistema bayesiano de diagnostico web")
    print("=" * 45)


def manual_query(network) -> None:
    variables = network.get_variables()
    print("\nVariables disponibles:")
    for index, name in enumerate(variables, start=1):
        print(f"{index}. {name}")

    selected = input("\nNumero de variable de consulta: ").strip()
    if not selected.isdigit() or not (1 <= int(selected) <= len(variables)):
        print("Seleccion invalida.")
        return

    query = variables[int(selected) - 1]
    evidence = {}
    print("\nIngresa evidencia (s = si, n = no, d = desconocido)")
    for variable in variables:
        if variable == query:
            continue
        raw = input(f"{variable}: ")
        value = parse_yes_no_unknown(raw)
        if value is None:
            continue
        evidence[variable] = value

    distribution = enumeration_ask(query, evidence, network)
    print_distribution(query, distribution)


def run_menu() -> None:
    network = create_web_diagnosis_network()
    while True:
        print_header()
        print("1. Ejecutar consulta manual")
        print("2. Ejecutar escenarios de prueba")
        print("3. Mostrar estructura de la red")
        print("4. Salir")
        option = input("\nSeleccione una opcion: ").strip()

        if option == "1":
            manual_query(network)
        elif option == "2":
            run_all_scenarios(network)
        elif option == "3":
            network.show_structure()
        elif option == "4":
            print("Saliendo...")
            break
        else:
            print("Opcion invalida.")

        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    run_menu()
