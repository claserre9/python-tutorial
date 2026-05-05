"""
Solutions — Chapitre 7
"""
import pytest
from dataclasses import dataclass, field
from functools import total_ordering


# 7.1 — Panier
class Panier:
    def __init__(self):
        self.articles = []

    def ajouter(self, item):
        self.articles.append(item)


p1, p2 = Panier(), Panier()
p1.ajouter("pomme")
assert p1.articles == ["pomme"]
assert p2.articles == []


# 7.2 — Date factory
class Date:
    def __init__(self, jour: int, mois: int, annee: int):
        self.jour = jour
        self.mois = mois
        self.annee = annee

    @classmethod
    def from_string(cls, s: str) -> "Date":
        j, m, a = map(int, s.split("-"))
        return cls(j, m, a)

    def __repr__(self):
        return f"Date({self.jour}, {self.mois}, {self.annee})"


d = Date.from_string("15-03-2026")
assert repr(d) == "Date(15, 3, 2026)"


# 7.3 — Vector2D
class Vector2D:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


v1, v2 = Vector2D(1, 2), Vector2D(3, 4)
assert v1 + v2 == Vector2D(4, 6)
assert abs(Vector2D(3, 4)) == 5.0
assert {Vector2D(1, 1)} == {Vector2D(1, 1)}


# 7.4 — Coord
@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int


positions = {Coord(0, 0): "start", Coord(5, 3): "end"}
assert positions[Coord(0, 0)] == "start"


# 7.5 — Personne validée
@dataclass
class Personne:
    nom: str
    age: int

    def __post_init__(self):
        if not 0 <= self.age <= 150:
            raise ValueError(f"age invalide: {self.age}")


Personne("Alice", 30)
with pytest.raises(ValueError):
    Personne("Bob", -1)
with pytest.raises(ValueError):
    Personne("Carol", 200)


# 7.6 — Temperature
class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("zéro absolu dépassé")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @property
    def kelvin(self) -> float:
        return self._celsius + 273.15


t = Temperature(20)
assert t.fahrenheit == 68.0
assert t.kelvin == 293.15
with pytest.raises(ValueError):
    t.celsius = -500


# 7.7 — Version avec total_ordering
@total_ordering
@dataclass
class Version:
    major: int
    minor: int
    patch: int

    def _key(self):
        return (self.major, self.minor, self.patch)

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._key() == other._key()

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._key() < other._key()


assert Version(1, 0, 0) < Version(1, 0, 1)
assert Version(1, 2, 0) > Version(1, 1, 9)
assert Version(2, 0, 0) >= Version(1, 99, 99)
assert sorted([Version(1, 2, 0), Version(1, 0, 0), Version(1, 1, 0)])[0] == Version(1, 0, 0)


print("Toutes les solutions passent ✅")
