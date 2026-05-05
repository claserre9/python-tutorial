"""Modèle Task."""
from dataclasses import dataclass, field
from typing import Literal

Priorite = Literal["bas", "moyen", "haut"]


@dataclass
class Task:
    # TODO : définir les champs
    # - id: int
    # - titre: str
    # - priorite: Priorite = "moyen"
    # - tags: list[str] = field(default_factory=list)
    # - terminee: bool = False
    ...

    # TODO : méthode to_dict() -> dict
    # TODO : classmethod from_dict(d: dict) -> Task
