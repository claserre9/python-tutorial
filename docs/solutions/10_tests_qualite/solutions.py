"""
Solutions — Chapitre 10
"""
import pytest
from typing import NewType, Literal, TypedDict


# 10.1 — Génériques
def dernier[T](items: list[T]) -> T:
    if not items:
        raise IndexError("liste vide")
    return items[-1]


assert dernier([1, 2, 3]) == 3
with pytest.raises(IndexError):
    dernier([])


# 10.2 — TypedDict
class UserDict(TypedDict):
    id: int
    nom: str
    actif: bool


def est_valide(u: UserDict) -> bool:
    return u["actif"] and u["id"] > 0


assert est_valide({"id": 1, "nom": "A", "actif": True}) is True
assert est_valide({"id": 0, "nom": "A", "actif": True}) is False
assert est_valide({"id": 1, "nom": "A", "actif": False}) is False


# 10.3 — NewType
UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)


def acheter(user: UserId, order: OrderId) -> str:
    return f"user {user} order {order}"


assert acheter(UserId(1), OrderId(42)) == "user 1 order 42"


# 10.4 — Literal
Priorite = Literal["bas", "moyen", "haut"]


def prioriser(p: Priorite) -> int:
    match p:
        case "bas":
            return 1
        case "moyen":
            return 2
        case "haut":
            return 3


assert prioriser("bas") == 1
assert prioriser("moyen") == 2
assert prioriser("haut") == 3


print("Toutes les solutions passent ✅")
