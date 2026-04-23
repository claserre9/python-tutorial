"""Modèle Task."""
from dataclasses import asdict, dataclass, field
from typing import Literal

Priorite = Literal["bas", "moyen", "haut"]


@dataclass
class Task:
    id: int
    titre: str
    priorite: Priorite = "moyen"
    tags: list[str] = field(default_factory=list)
    terminee: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        return cls(
            id=d["id"],
            titre=d["titre"],
            priorite=d.get("priorite", "moyen"),
            tags=list(d.get("tags", [])),
            terminee=bool(d.get("terminee", False)),
        )
