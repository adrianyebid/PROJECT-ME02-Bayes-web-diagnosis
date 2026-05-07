from __future__ import annotations

from bayesian_network import BayesianNetwork
from node import Node


def create_web_diagnosis_network() -> BayesianNetwork:
    network = BayesianNetwork()

    nodes = [
        Node("BaseDatosCaida", [], {(): 0.05}),
        Node("BackendSaturado", [], {(): 0.10}),
        Node("GatewayCaido", [], {(): 0.04}),
        Node("ConexionInestable", [], {(): 0.12}),
        Node("ErrorAutenticacion", [], {(): 0.08}),
        Node(
            "Error500",
            ["BaseDatosCaida", "BackendSaturado"],
            {
                (True, True): 0.95,
                (True, False): 0.85,
                (False, True): 0.70,
                (False, False): 0.05,
            },
        ),
        Node(
            "LatenciaAlta",
            ["GatewayCaido", "ConexionInestable"],
            {
                (True, True): 0.90,
                (True, False): 0.75,
                (False, True): 0.65,
                (False, False): 0.10,
            },
        ),
        Node(
            "LoginFallido",
            ["ErrorAutenticacion"],
            {
                (True,): 0.90,
                (False,): 0.08,
            },
        ),
        Node(
            "ServicioNoDisponible",
            ["GatewayCaido", "BackendSaturado", "BaseDatosCaida"],
            {
                (True, True, True): 0.98,
                (True, True, False): 0.92,
                (True, False, True): 0.95,
                (True, False, False): 0.80,
                (False, True, True): 0.90,
                (False, True, False): 0.65,
                (False, False, True): 0.75,
                (False, False, False): 0.03,
            },
        ),
        Node(
            "UsuarioAfectado",
            ["Error500", "LatenciaAlta"],
            {
                (True, True): 0.95,
                (True, False): 0.80,
                (False, True): 0.60,
                (False, False): 0.05,
            },
        ),
    ]

    for node in nodes:
        network.add_node(node)
    network.validate_network()
    return network
