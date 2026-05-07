from __future__ import annotations

from typing import Dict, List

from bayesian_network import BayesianNetwork


def enumeration_ask(
    query: str, evidence: Dict[str, bool], network: BayesianNetwork
) -> Dict[bool, float]:
    if query in evidence:
        raise ValueError("La variable de consulta no debe estar incluida en la evidencia.")

    distribution: Dict[bool, float] = {}
    for value in (True, False):
        extended_evidence = dict(evidence)
        extended_evidence[query] = value
        distribution[value] = enumerate_all(
            network.get_variables(), extended_evidence, network
        )
    return normalize(distribution)


def enumerate_all(
    variables: List[str], evidence: Dict[str, bool], network: BayesianNetwork
) -> float:
    if not variables:
        return 1.0

    first, rest = variables[0], variables[1:]
    if first in evidence:
        probability = network.probability(first, evidence[first], evidence)
        return probability * enumerate_all(rest, evidence, network)

    total = 0.0
    for value in (True, False):
        extended_evidence = dict(evidence)
        extended_evidence[first] = value
        probability = network.probability(first, value, extended_evidence)
        total += probability * enumerate_all(rest, extended_evidence, network)
    return total


def normalize(distribution: Dict[bool, float]) -> Dict[bool, float]:
    total = sum(distribution.values())
    if total == 0.0:
        raise ValueError("No se puede normalizar una distribucion con suma 0.")
    return {key: value / total for key, value in distribution.items()}
