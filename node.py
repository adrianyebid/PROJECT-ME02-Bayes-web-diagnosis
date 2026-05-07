from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class Node:
    name: str
    parents: List[str] = field(default_factory=list)
    cpt: Dict[Tuple[bool, ...], float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.validate_cpt()

    def validate_cpt(self) -> None:
        expected_rows = 2 ** len(self.parents)
        if len(self.cpt) != expected_rows:
            raise ValueError(
                f"CPT de '{self.name}' invalida: se esperaban {expected_rows} filas y se recibieron {len(self.cpt)}."
            )
        for key, probability in self.cpt.items():
            if len(key) != len(self.parents):
                raise ValueError(
                    f"CPT de '{self.name}' invalida: llave {key} no coincide con cantidad de padres."
                )
            if not (0.0 <= probability <= 1.0):
                raise ValueError(
                    f"CPT de '{self.name}' invalida: probabilidad fuera de rango para {key}: {probability}."
                )

    def get_probability(self, value: bool, evidence: Dict[str, bool]) -> float:
        parent_values = tuple(evidence[parent] for parent in self.parents)
        p_true = self.cpt[parent_values]
        return p_true if value else 1.0 - p_true

    def __repr__(self) -> str:
        return f"Node(name='{self.name}', parents={self.parents})"
