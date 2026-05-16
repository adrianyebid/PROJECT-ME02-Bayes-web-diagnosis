from __future__ import annotations

from typing import Dict, List

from node import Node


class BayesianNetwork:
    """
    Almacena, gestiona y valida la estructura de una red bayesiana.

    Esta clase mantiene el conjunto de nodos y asegura que se respete el orden
    topológico de las variables, el cual es fundamental para el algoritmo de inferencia.
    
    Attributes:
        nodes (Dict[str, Node]): Diccionario que asocia el nombre de la variable con su objeto Node correspondiente.
        order (List[str]): Lista que mantiene los nombres de los nodos en el orden en que fueron insertados.
                           Sirve como el orden topológico requerido, asumiendo que los nodos se insertan
                           desde las causas hacia los síntomas (los padres antes que los hijos).
    """
    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        self.order: List[str] = []

    def add_node(self, node: Node) -> None:
        if node.name in self.nodes:
            raise ValueError(f"El nodo '{node.name}' ya existe en la red.")
        self.nodes[node.name] = node
        self.order.append(node.name)

    def get_node(self, name: str) -> Node:
        if name not in self.nodes:
            raise KeyError(f"El nodo '{name}' no existe en la red.")
        return self.nodes[name]

    def get_variables(self) -> List[str]:
        return list(self.order)

    def get_parents(self, variable: str) -> List[str]:
        return list(self.get_node(variable).parents)

    def probability(self, variable: str, value: bool, evidence: Dict[str, bool]) -> float:
        return self.get_node(variable).get_probability(value, evidence)

    def validate_network(self) -> None:
        for name in self.order:
            node = self.nodes[name]
            for parent in node.parents:
                if parent not in self.nodes:
                    raise ValueError(
                        f"El nodo '{name}' tiene un padre inexistente: '{parent}'."
                    )
                if self.order.index(parent) >= self.order.index(name):
                    raise ValueError(
                        f"El nodo '{name}' esta antes que su padre '{parent}' en el orden topologico."
                    )

    def show_structure(self) -> None:
        print("\nEstructura de la red bayesiana:")
        for variable in self.order:
            parents = self.nodes[variable].parents
            if parents:
                print(f"- {variable} <- {', '.join(parents)}")
            else:
                print(f"- {variable} <- (sin padres)")
