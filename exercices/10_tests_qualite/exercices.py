"""
Exercices — Chapitre 10 : Typage & qualité

Note : ces exercices sont surtout des vérifications conceptuelles. Le vrai
travail de ce chapitre est le projet fil rouge (dossier logparser/).
"""
import pytest
from typing import Protocol, TypedDict, NewType, Literal


# =============================================================================
# 10.1 — TypeVar / génériques (PEP 695 syntax)
# =============================================================================
# Écrivez `dernier[T](items: list[T]) -> T` qui retourne le dernier élément.
# Si la liste est vide, lever IndexError.

def dernier[T](items: list[T]) -> T:
    ...  # TODO


assert dernier([1, 2, 3]) == 3
assert dernier(["a", "b"]) == "b"
with pytest.raises(IndexError):
    dernier([])


# =============================================================================
# 10.2 — TypedDict
# =============================================================================
# Définissez un TypedDict `UserDict` avec id (int), nom (str), actif (bool).
# Puis écrivez une fonction `est_valide(u: UserDict) -> bool` qui retourne
# True si actif est True ET id > 0.

class UserDict(TypedDict):
    ...  # TODO


def est_valide(u: UserDict) -> bool:
    ...  # TODO


assert est_valide({"id": 1, "nom": "A", "actif": True}) is True
assert est_valide({"id": 0, "nom": "A", "actif": True}) is False
assert est_valide({"id": 1, "nom": "A", "actif": False}) is False


# =============================================================================
# 10.3 — NewType
# =============================================================================
# Créez UserId et OrderId en NewType(..., int).
# Écrivez `acheter(user: UserId, order: OrderId) -> str` qui retourne
# f"user {user} order {order}".

UserId = ...   # TODO
OrderId = ...  # TODO


def acheter(user: UserId, order: OrderId) -> str:
    return f"user {user} order {order}"


u = UserId(1)
o = OrderId(42)
assert acheter(u, o) == "user 1 order 42"

# Note : mypy refuserait acheter(o, u), mais à l'exécution ça marche
# (NewType est purement statique).


# =============================================================================
# 10.4 — Literal
# =============================================================================
# Définissez un type `Priorite` = Literal["bas", "moyen", "haut"].
# Écrivez `prioriser(p: Priorite) -> int` qui retourne 1/2/3.

Priorite = ...  # TODO


def prioriser(p: Priorite) -> int:
    ...  # TODO : utiliser un match


assert prioriser("bas") == 1
assert prioriser("moyen") == 2
assert prioriser("haut") == 3


# =============================================================================
# 10.5 — Test parametrize (à lancer avec pytest)
# =============================================================================
# Pour cet exercice, créez un fichier test_calcul.py à côté et lancez pytest.
# On vous donne juste la fonction à tester.

def additionner(a: int, b: int) -> int:
    return a + b


# Dans un test_calcul.py, vous écririez :
#
# import pytest
# from exercices import additionner
#
# @pytest.mark.parametrize("a, b, attendu", [
#     (1, 2, 3),
#     (0, 0, 0),
#     (-5, 5, 0),
# ])
# def test_additionner(a, b, attendu):
#     assert additionner(a, b) == attendu


# =============================================================================
# 10.6 — Fixture pytest
# =============================================================================
# Écrivez une fixture qui crée un fichier temporaire avec un contenu donné
# et le retourne. Utilisez tmp_path.
# Puis écrivez un test qui vérifie que lire(chemin) retourne le contenu.

from pathlib import Path


def lire(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# Dans un test_fichier.py :
#
# @pytest.fixture
# def fichier_temp(tmp_path):
#     p = tmp_path / "demo.txt"
#     p.write_text("coucou", encoding="utf-8")
#     return p
#
# def test_lire(fichier_temp):
#     assert lire(fichier_temp) == "coucou"


if __name__ == "__main__":
    print("Tous les tests passent ✅")
