from __future__ import annotations

from typing import Dict, Optional

TRUE_INPUTS = {"s", "si", "y", "yes", "true", "1"}
FALSE_INPUTS = {"n", "no", "false", "0"}
UNKNOWN_INPUTS = {"d", "desconocido", "", "?"}


def bool_to_spanish(value: bool) -> str:
    return "si" if value else "no"


def parse_yes_no_unknown(text: str) -> Optional[bool]:
    normalized = text.strip().lower()
    if normalized in TRUE_INPUTS:
        return True
    if normalized in FALSE_INPUTS:
        return False
    if normalized in UNKNOWN_INPUTS:
        return None
    return None


def is_valid_yes_no_unknown_input(text: str) -> bool:
    normalized = text.strip().lower()
    return normalized in TRUE_INPUTS | FALSE_INPUTS | UNKNOWN_INPUTS


def format_probability(value: float) -> str:
    return f"{value:.4f} ({value * 100:.2f}%)"


def print_evidence(evidence: Dict[str, bool]) -> None:
    if not evidence:
        print("Evidencia: (sin evidencia)")
        return
    print("Evidencia:")
    for variable, value in evidence.items():
        print(f"  - {variable} = {bool_to_spanish(value)}")


def print_distribution(query: str, distribution: Dict[bool, float]) -> None:
    print(f"Resultado para {query}:")
    print(f"  P({query}=si | evidencia) = {format_probability(distribution[True])}")
    print(f"  P({query}=no | evidencia) = {format_probability(distribution[False])}")
