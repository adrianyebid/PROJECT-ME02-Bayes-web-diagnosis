from __future__ import annotations

import os
from typing import Any, Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

GRAPHS_DIR = "graphs"


def _ensure_graphs_dir() -> None:
    os.makedirs(GRAPHS_DIR, exist_ok=True)


def _spanish_label(var_name: str) -> str:
    labels = {
        "BaseDatosCaida": "BD caida",
        "BackendSaturado": "Backend saturado",
        "GatewayCaido": "Gateway caido",
        "ConexionInestable": "Conexion inestable",
        "ErrorAutenticacion": "Error autenticacion",
        "Error500": "Error 500",
        "LatenciaAlta": "Latencia alta",
        "LoginFallido": "Login fallido",
        "ServicioNoDisponible": "Servicio no disponible",
        "UsuarioAfectado": "Usuario afectado",
    }
    return labels.get(var_name, var_name)


def plot_scenario_comparison(scenario_results: List[Dict[str, Any]]) -> str:
    _ensure_graphs_dir()

    names = [r["name"] for r in scenario_results]
    p_true_values = [r["p_true"] for r in scenario_results]

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#2196F3", "#FF9800", "#4CAF50", "#9C27B0", "#F44336"]
    bars = ax.bar(range(len(names)), p_true_values, color=colors, edgecolor="white", linewidth=1.2)

    for bar, val in zip(bars, p_true_values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f"{val:.4f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=15, ha="right", fontsize=10)
    ax.set_ylabel("P(causa = si | evidencia)", fontsize=12)
    ax.set_title("Comparacion de escenarios: probabilidad posterior de cada causa", fontsize=14, fontweight="bold")
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.3)

    filepath = os.path.join(GRAPHS_DIR, "comparacion_escenarios.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"Grafico guardado: {filepath}")
    return filepath


def plot_prior_vs_posterior(
    scenario_results: List[Dict[str, Any]],
    prior_values: Dict[str, float],
) -> str:
    _ensure_graphs_dir()

    queries = [r["query"] for r in scenario_results]
    x = range(len(queries))
    width = 0.35

    priors = [prior_values[q] for q in queries]
    posteriors = [r["p_true"] for r in scenario_results]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar([i - width / 2 for i in x], priors, width, label="P(si) a priori",
                    color="#90CAF9", edgecolor="white", linewidth=1.2)
    bars2 = ax.bar([i + width / 2 for i in x], posteriors, width, label="P(si | evidencia)",
                    color="#1565C0", edgecolor="white", linewidth=1.2)

    for bar, val in zip(bars1, priors):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                f"{val:.4f}", ha="center", va="bottom", fontsize=9)
    for bar, val in zip(bars2, posteriors):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                f"{val:.4f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([_spanish_label(q) for q in queries], fontsize=10)
    ax.set_ylabel("Probabilidad", fontsize=12)
    ax.set_title("Probabilidad a priori vs a posteriori para cada causa", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.3)

    filepath = os.path.join(GRAPHS_DIR, "priori_vs_posteriori.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"Grafico guardado: {filepath}")
    return filepath


def plot_sensitivity_bars(sensitivity_results: List[Dict[str, Any]]) -> List[str]:
    _ensure_graphs_dir()
    saved = []

    for scenario_data in sensitivity_results:
        scenario_name = scenario_data["scenario"]
        query = scenario_data["query"]
        variations = scenario_data["variations"]

        labels = [v["label"] for v in variations]
        p_true_vals = [v["p_true"] for v in variations]

        shortened_labels = []
        for label in labels:
            if len(label) > 40:
                label = label[:37] + "..."
            shortened_labels.append(label)

        fig, ax = plt.subplots(figsize=(14, max(6, len(variations) * 0.5)))
        colors = plt.cm.viridis([i / len(variations) for i in range(len(variations))])
        y_positions = range(len(variations))

        bars = ax.barh(y_positions, p_true_vals, color=colors, edgecolor="white", linewidth=1.2)

        for bar, val in zip(bars, p_true_vals):
            ax.text(
                bar.get_width() + 0.005,
                bar.get_y() + bar.get_height() / 2,
                f"{val:.4f}",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

        ax.set_yticks(y_positions)
        ax.set_yticklabels(shortened_labels, fontsize=9)
        ax.set_xlabel(f"P({query}=si | evidencia)", fontsize=12)
        ax.set_title(f"Sensibilidad: {scenario_name}", fontsize=13, fontweight="bold")
        ax.set_xlim(0, 1.05)
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=0.3)

        safe_name = scenario_name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        filepath = os.path.join(GRAPHS_DIR, f"sensibilidad_{safe_name}.png")
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Grafico guardado: {filepath}")
        saved.append(filepath)

    return saved


def plot_execution_times(scenario_results: List[Dict[str, Any]]) -> str:
    _ensure_graphs_dir()

    names = [r["name"] for r in scenario_results]
    times = [r["time_ms"] for r in scenario_results]

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#2196F3", "#FF9800", "#4CAF50", "#9C27B0", "#F44336"]
    bars = ax.bar(range(len(names)), times, color=colors, edgecolor="white", linewidth=1.2)

    for bar, val in zip(bars, times):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.002,
            f"{val:.2f} ms",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=15, ha="right", fontsize=10)
    ax.set_ylabel("Tiempo (ms)", fontsize=12)
    ax.set_title("Tiempos de ejecucion por escenario", fontsize=14, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)

    filepath = os.path.join(GRAPHS_DIR, "tiempos_ejecucion.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"Grafico guardado: {filepath}")
    return filepath


def plot_sensitivity_heatmap(sensitivity_results: List[Dict[str, Any]]) -> str:
    _ensure_graphs_dir()

    num_scenarios = len(sensitivity_results)
    fig, axes = plt.subplots(num_scenarios, 1, figsize=(14, 3.5 * num_scenarios))

    if num_scenarios == 1:
        axes = [axes]

    for ax, scenario_data in zip(axes, sensitivity_results):
        scenario_name = scenario_data["scenario"]
        query = scenario_data["query"]
        variations = scenario_data["variations"]

        labels = [v["label"] for v in variations]
        p_true_vals = [v["p_true"] for v in variations]

        short_labels = []
        for label in labels:
            words = label.split()
            if len(words) > 3:
                label = " ".join(words[:3]) + "..."
            short_labels.append(label)

        colors = ["#4CAF50" if v > 0.5 else "#F44336" if v < 0.2 else "#FF9800" for v in p_true_vals]
        y_positions = range(len(variations))

        bars = ax.barh(y_positions, p_true_vals, color=colors, edgecolor="white", linewidth=1)
        ax.axvline(x=0.5, color="gray", linestyle="--", alpha=0.5, linewidth=1)

        for bar, val in zip(bars, p_true_vals):
            ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2,
                    f"{val:.4f}", va="center", fontsize=9, fontweight="bold")

        ax.set_yticks(y_positions)
        ax.set_yticklabels(short_labels, fontsize=8)
        ax.set_xlabel(f"P({query}=si | evidencia)", fontsize=10)
        ax.set_title(f"{scenario_name}", fontsize=11, fontweight="bold")
        ax.set_xlim(0, 1.05)
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=0.3)

    plt.suptitle("Analisis de sensibilidad completo", fontsize=14, fontweight="bold", y=1.01)
    filepath = os.path.join(GRAPHS_DIR, "sensibilidad_completa.png")
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Grafico guardado: {filepath}")
    return filepath


def print_ascii_network_diagram() -> str:
    diagram = (
        "\n"
        "          RED BAYESIANA: DIAGNOSTICO DE FALLAS WEB\n"
        "          =========================================\n"
        "\n"
        "                    +------------------+\n"
        "                    | BaseDatosCaida   |---- prior: P(si)=0.05\n"
        "                    +-------+----------+\n"
        "                            |\n"
        "          +-----------------+---------------------+\n"
        "          |                 |                     |\n"
        "          v                 v                     |\n"
        "  +------------------+  +------------------+      |\n"
        "  | BackendSaturado  |  |  GatewayCaido    |      |\n"
        "  | prior:P(si)=0.10 |  | prior:P(si)=0.04 |      |\n"
        "  +--+------+--------+  +--+--------+------+      |\n"
        "     |      |              |        |             |\n"
        "     |      |       +------+        |             |\n"
        "     |      |       |               |             |\n"
        "     v      |       v               v             |\n"
        "  +-----------+ | +-----------------------+       |\n"
        "  |  Error500 | | |   LatenciaAlta        |       |\n"
        "  | padres:   | | | padres: GatewayCaido, |       |\n"
        "  | BD,Backend| | | ConexionInestable     |       |\n"
        "  +-----+-----+ | +-----+-----------------+       |\n"
        "        |        |       |                         |\n"
        "        |        |  +----+                         |\n"
        "        +---+    |  |    +----------------------+  |\n"
        "            |    |  |    |ConexionInestable     |  |\n"
        "            v    |  v    |prior: P(si)=0.12     |  |\n"
        "  +-------------------+ +----------+------------+  |\n"
        "  | UsuarioAfectado   |            |               |\n"
        "  | padres:Error500,  |            |               |\n"
        "  | LatenciaAlta      |            |               |\n"
        "  +-------------------+            |               |\n"
        "                                   |               |\n"
        "  +-------------------+            |               |\n"
        "  |ErrorAutenticacion |            |               |\n"
        "  |prior:P(si)=0.08   |            |               |\n"
        "  +--------+----------+            |               |\n"
        "           |                       |               |\n"
        "           v                       |               |\n"
        "  +-------------------+            |               |\n"
        "  |  LoginFallido     |            |               |\n"
        "  | padre:ErrorAutent |            |               |\n"
        "  +-------------------+            |               |\n"
        "                                   |               |\n"
        "          +------------------------+---------------+\n"
        "          |                        |\n"
        "          v                        v\n"
        "  +--------------------------------------------------+\n"
        "  |        ServicioNoDisponible                      |\n"
        "  | padres: GatewayCaido, BackendSaturado,           |\n"
        "  |         BaseDatosCaida                           |\n"
        "  +--------------------------------------------------+\n"
        "\n"
        "  CAUSAS (nodos raiz)           SINTOMAS (nodos hoja/intermedios)\n"
        "  --------------------          ---------------------------------\n"
        "  BaseDatosCaida                Error500\n"
        "  BackendSaturado               LatenciaAlta\n"
        "  GatewayCaido                  LoginFallido\n"
        "  ConexionInestable             ServicioNoDisponible\n"
        "  ErrorAutenticacion            UsuarioAfectado\n"
    )
    print(diagram)
    return diagram


def print_ascii_inference_flow() -> str:
    diagram = (
        "\n"
        "   FLUJO DEL ALGORITMO DE INFERENCIA POR ENUMERACION\n"
        "   ==================================================\n"
        "\n"
        "   +--------------------------------------------------+\n"
        "   |        enumeration_ask(query, evidence, network) |\n"
        "   |                                                   |\n"
        "   |  Entrada:                                         |\n"
        "   |    - query: variable a consultar (ej:            |\n"
        "   |      BaseDatosCaida)                              |\n"
        "   |    - evidence: diccionario de sintomas            |\n"
        "   |      observados                                   |\n"
        "   |    - network: red bayesiana con CPTs              |\n"
        "   +---------------------+-----------------------------+\n"
        "                         |\n"
        "                         v\n"
        "   +--------------------------------------------------+\n"
        "   |  Para cada valor v en {True, False}:              |\n"
        "   |                                                   |\n"
        "   |    1. Extender evidencia con {query: v}           |\n"
        "   |    2. Llamar a enumerate_all()                    |\n"
        "   |    3. Guardar resultado en distribution[v]        |\n"
        "   +---------------------+-----------------------------+\n"
        "                         |\n"
        "                         v\n"
        "   +--------------------------------------------------+\n"
        "   |         enumerate_all(vars, evidence, network)    |\n"
        "   |                                                   |\n"
        "   |  Caso base (vars vacio):                          |\n"
        "   |    return 1.0                                     |\n"
        "   |                                                   |\n"
        "   |  Variable observada (en evidence):                |\n"
        "   |    prob = CPT(var | padres en evidence)           |\n"
        "   |    return prob * enumerate_all(resto, ev, net)   |\n"
        "   |                                                   |\n"
        "   |  Variable oculta (no en evidence):                |\n"
        "   |    total = 0.0                                    |\n"
        "   |    Para cada valor en {True, False}:              |\n"
        "   |      extender evidence con {var: valor}           |\n"
        "   |      prob = CPT(var | padres en evidence_ext)    |\n"
        "   |      total += prob * enumerate_all(resto, ev, net)|\n"
        "   |    return total                                   |\n"
        "   +---------------------+-----------------------------+\n"
        "                         |\n"
        "                         v\n"
        "   +--------------------------------------------------+\n"
        "   |           normalize(distribution)                 |\n"
        "   |                                                   |\n"
        "   |  total = sum(distribution.values())               |\n"
        "   |  return {k: v/total for k, v in distribution}    |\n"
        "   |                                                   |\n"
        "   |  Resultado: P(query=si|evidence) y                |\n"
        "   |             P(query=no|evidence)                  |\n"
        "   |  Verifica que P(si) + P(no) = 1.0                 |\n"
        "   +--------------------------------------------------+\n"
    )
    print(diagram)
    return diagram


def print_ascii_system_blocks() -> str:
    diagram = (
        "\n"
        "   DIAGRAMA DE BLOQUES DEL SISTEMA\n"
        "   ================================\n"
        "\n"
        "   +----------+\n"
        "   | USUARIO  |\n"
        "   +-----+----+\n"
        "         |\n"
        "         v\n"
        "   +--------------------------------------------------+\n"
        "   |           MENU DE CONSOLA                         |\n"
        "   |  (main.py: entrada/salida interactiva)            |\n"
        "   +---------------------+----------------------------+\n"
        "                         |\n"
        "          +--------------+--------------+\n"
        "          |              |              |\n"
        "          v              v              v\n"
        "   +-----------+ +-----------+ +------------------+\n"
        "   | Consulta  | |Escenarios | |Sensibilidad/     |\n"
        "   | manual    | |predefin.  | |analisis completo |\n"
        "   +-----+-----+ +-----+-----+ +--------+---------+\n"
        "         |              |               |\n"
        "         +--------------+---------------+\n"
        "                        |\n"
        "                        v\n"
        "   +--------------------------------------------------+\n"
        "   |      MOTOR DE INFERENCIA BAYESIANA               |\n"
        "   |  (inference.py)                                  |\n"
        "   |                                                   |\n"
        "   |  enumeration_ask() --> enumerate_all()            |\n"
        "   |                    --> normalize()                |\n"
        "   +---------------------+----------------------------+\n"
        "                         |\n"
        "                         v\n"
        "   +--------------------------------------------------+\n"
        "   |         RED BAYESIANA + CPT                       |\n"
        "   |  (bayesian_network.py + node.py + model.py)       |\n"
        "   |                                                   |\n"
        "   |  10 nodos, 5 causas, 5 sintomas                  |\n"
        "   |  CPTs con probabilidades condicionales            |\n"
        "   +---------------------+----------------------------+\n"
        "                         |\n"
        "                         v\n"
        "   +--------------------------------------------------+\n"
        "   |      RESULTADOS PROBABILISTICOS                   |\n"
        "   |                                                   |\n"
        "   |  P(Causa=si | Evidencia) = X.XXXX                |\n"
        "   |  P(Causa=no | Evidencia) = Y.YYYY                |\n"
        "   +---------------------+----------------------------+\n"
        "                         |\n"
        "                         v\n"
        "   +--------------------------------------------------+\n"
        "   |   ANALISIS E INTERPRETACION                       |\n"
        "   |                                                   |\n"
        "   |  - Comparacion a priori vs a posteriori           |\n"
        "   |  - Sensibilidad de evidencia                      |\n"
        "   |  - Graficos (visualization.py)                    |\n"
        "   |  - Exportacion JSON                               |\n"
        "   +--------------------------------------------------+\n"
    )
    print(diagram)
    return diagram


def generate_all_charts(
    scenario_results: List[Dict[str, Any]],
    sensitivity_results: List[Dict[str, Any]],
    prior_values: Dict[str, float],
) -> List[str]:
    _ensure_graphs_dir()
    saved_files = []

    print("\n=== Generando graficos ===")

    saved_files.append(plot_scenario_comparison(scenario_results))
    saved_files.append(plot_prior_vs_posterior(scenario_results, prior_values))
    saved_files.append(plot_execution_times(scenario_results))
    saved_files.append(plot_sensitivity_heatmap(sensitivity_results))
    saved_files.extend(plot_sensitivity_bars(sensitivity_results))

    print(f"\nSe generaron {len(saved_files)} graficos en el directorio '{GRAPHS_DIR}/'.")
    return saved_files


def generate_all_ascii_diagrams() -> None:
    print("\n=== Diagramas de flujo (ASCII) ===")
    print_ascii_system_blocks()
    print_ascii_network_diagram()
    print_ascii_inference_flow()
