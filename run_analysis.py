from __future__ import annotations

from inference import enumeration_ask
from model import create_web_diagnosis_network
from scenarios import run_full_analysis
from visualization import generate_all_ascii_diagrams, generate_all_charts


def main() -> None:
    print("=" * 55)
    print("ANALISIS COMPLETO - INTEGRANTE 6")
    print("Escenarios de prueba, sensibilidad y graficos")
    print("=" * 55)

    network = create_web_diagnosis_network()

    results = run_full_analysis(network)

    prior_values = {}
    for scenario in results["escenarios_base"]:
        q = scenario["query"]
        if q not in prior_values:
            dist = enumeration_ask(q, {}, network)
            prior_values[q] = dist[True]

    print("\n" + "=" * 55)
    print("GENERANDO GRAFICOS (MATPLOTLIB)")
    print("=" * 55)
    generate_all_charts(
        results["escenarios_base"],
        results["analisis_sensibilidad"],
        prior_values,
    )

    print("\n" + "=" * 55)
    print("GENERANDO DIAGRAMAS DE FLUJO (ASCII)")
    print("=" * 55)
    generate_all_ascii_diagrams()

    print("\n" + "=" * 55)
    print("PROCESO COMPLETO FINALIZADO")
    print("=" * 55)
    print("\nArchivos generados:")
    print("  - graphs/comparacion_escenarios.png")
    print("  - graphs/priori_vs_posteriori.png")
    print("  - graphs/tiempos_ejecucion.png")
    print("  - graphs/sensibilidad_completa.png")
    print("  - graphs/sensibilidad_*.png (5 archivos)")
    print("  - resultados_escenarios.json")


if __name__ == "__main__":
    main()
