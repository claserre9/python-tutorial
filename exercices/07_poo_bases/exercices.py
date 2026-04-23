"""
Exercices — Chapitre 7 : POO bases
"""
from dataclasses import dataclass, field
from functools import total_ordering


# =============================================================================
# 7.1 — Le piège de l'attribut de classe mutable
# =============================================================================
# La classe Panier ci-dessous a le bug classique. Corrigez-la.

class PanierCasse:
    articles = []     # ❌
    def ajouter(self, item):
        self.articles.append(item)


class Panier:
    # TODO : corriger en initialisant articles dans __init__
    ...


p1, p2 = Panier(), Panier()
p1.ajouter("pomme")
assert p1.articles == ["pomme"]
assert p2.articles == []


# =============================================================================
# 7.2 — Classmethod factory
# =============================================================================
# Implémentez Date avec :
#  - __init__(jour, mois, annee)
#  - classmethod from_string("JJ-MM-AAAA")
#  - __repr__ donnant "Date(15, 3, 2026)"

class Date:
    ...  # TODO


d = Date.from_string("15-03-2026")
assert d.jour == 15 and d.mois == 3 and d.annee == 2026
assert repr(d) == "Date(15, 3, 2026)"


# =============================================================================
# 7.3 — Dunders : Vector
# =============================================================================
# Implémentez Vector2D avec :
#  - __init__(x, y)
#  - __repr__ -> "Vector2D(x, y)"
#  - __eq__ structurel
#  - __hash__ cohérent
#  - __add__ pour que Vector2D(1, 2) + Vector2D(3, 4) == Vector2D(4, 6)
#  - __abs__ -> norme euclidienne

class Vector2D:
    ...  # TODO


v1, v2 = Vector2D(1, 2), Vector2D(3, 4)
assert v1 + v2 == Vector2D(4, 6)
assert Vector2D(3, 4) == Vector2D(3, 4)
assert hash(Vector2D(3, 4)) == hash(Vector2D(3, 4))
assert {Vector2D(1, 1)} == {Vector2D(1, 1)}
assert abs(Vector2D(3, 4)) == 5.0
assert repr(v1) == "Vector2D(1, 2)"


# =============================================================================
# 7.4 — Dataclass frozen hashable
# =============================================================================
# Définissez Coord comme dataclass frozen+slots avec x, y: int.
# Puis utilisez Coord comme clé d'un dict.

# TODO
@dataclass  # options ?
class Coord:
    ...


positions = {Coord(0, 0): "start", Coord(5, 3): "end"}
assert positions[Coord(0, 0)] == "start"


# =============================================================================
# 7.5 — Validation via __post_init__
# =============================================================================
# Définissez Personne(nom: str, age: int) en dataclass.
# Dans __post_init__, valider : age entre 0 et 150. Sinon ValueError.

# TODO
@dataclass
class Personne:
    ...


Personne("Alice", 30)       # OK

import pytest
with pytest.raises(ValueError):
    Personne("Bob", -1)
with pytest.raises(ValueError):
    Personne("Carol", 200)


# =============================================================================
# 7.6 — @property : Temperature avec setter
# =============================================================================
# Temperature(celsius) :
#  - celsius : getter + setter qui refuse < -273.15
#  - fahrenheit : propriété dérivée lecture seule (c*9/5 + 32)
#  - kelvin : propriété dérivée lecture seule (c + 273.15)

class Temperature:
    ...  # TODO


t = Temperature(20)
assert t.celsius == 20
assert t.fahrenheit == 68.0
assert t.kelvin == 293.15

t.celsius = 100
assert t.fahrenheit == 212.0

with pytest.raises(ValueError):
    t.celsius = -500


# =============================================================================
# 7.7 — total_ordering
# =============================================================================
# Classe Version(major, minor, patch) qui se trie sémantiquement.
# Implémentez __eq__ et __lt__ seulement, laissez total_ordering générer le reste.

@total_ordering
class Version:
    ...  # TODO


assert Version(1, 0, 0) < Version(1, 0, 1)
assert Version(1, 2, 0) > Version(1, 1, 9)
assert Version(2, 0, 0) >= Version(1, 99, 99)
assert Version(1, 0, 0) == Version(1, 0, 0)
assert sorted([Version(1, 2, 0), Version(1, 0, 0), Version(1, 1, 0)])[0] == Version(1, 0, 0)


if __name__ == "__main__":
    print("Tous les tests passent ✅")
