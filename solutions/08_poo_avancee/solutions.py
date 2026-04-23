"""
Solutions — Chapitre 8
"""
import contextlib
import io
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import pi, isclose
from typing import Protocol, runtime_checkable

import pytest


# 8.1 — MRO coopératif
class A:
    def __init__(self):
        print("A")
        super().__init__()     # appelle object.__init__

class B(A):
    def __init__(self):
        print("B")
        super().__init__()

class C(A):
    def __init__(self):
        print("C")
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D")
        super().__init__()


buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    D()
assert buf.getvalue() == "D\nB\nC\nA\n"
assert [c.__name__ for c in D.__mro__] == ["D", "B", "C", "A", "object"]


# 8.2 — Forme
class Forme(ABC):
    @abstractmethod
    def aire(self) -> float: ...

    @abstractmethod
    def perimetre(self) -> float: ...


class Rectangle(Forme):
    def __init__(self, l, h):
        self.l, self.h = l, h

    def aire(self): return self.l * self.h
    def perimetre(self): return 2 * (self.l + self.h)


class Cercle(Forme):
    def __init__(self, r):
        self.r = r

    def aire(self): return pi * self.r ** 2
    def perimetre(self): return 2 * pi * self.r


with pytest.raises(TypeError):
    Forme()
assert Rectangle(3, 4).aire() == 12
assert isclose(Cercle(5).aire(), pi * 25)


# 8.3 — Protocol
@runtime_checkable
class Serialisable(Protocol):
    def to_dict(self) -> dict: ...


class Produit:
    def __init__(self, nom, prix):
        self.nom, self.prix = nom, prix

    def to_dict(self) -> dict:
        return {"nom": self.nom, "prix": self.prix}


class Event:
    def __init__(self, titre):
        self.titre = titre

    def to_dict(self) -> dict:
        return {"titre": self.titre}


def exporter(obj: Serialisable) -> dict:
    return obj.to_dict()


assert exporter(Produit("laptop", 1200)) == {"nom": "laptop", "prix": 1200}
assert exporter(Event("conf")) == {"titre": "conf"}
assert isinstance(Produit("a", 1), Serialisable)


# 8.4 — Composition
class Notifier(ABC):
    @abstractmethod
    def envoyer(self, dest: str, msg: str) -> None: ...


class FakeNotifier(Notifier):
    def __init__(self):
        self.envois: list[tuple[str, str]] = []

    def envoyer(self, dest, msg):
        self.envois.append((dest, msg))


class UserService:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def bienvenue(self, user_email: str) -> None:
        self.notifier.envoyer(user_email, "Bienvenue !")


fake = FakeNotifier()
svc = UserService(fake)
svc.bienvenue("alice@a.com")
svc.bienvenue("bob@b.com")
assert fake.envois == [("alice@a.com", "Bienvenue !"), ("bob@b.com", "Bienvenue !")]


# 8.5 — kw_only
@dataclass(kw_only=True)
class Base:
    x: int


@dataclass(kw_only=True)
class Derived(Base):
    y: int = 0


d = Derived(x=5)
assert d.x == 5 and d.y == 0


# 8.6 — slots
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


class PointSlot:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y


def taille_totale(obj):
    total = sys.getsizeof(obj)
    if hasattr(obj, "__dict__"):
        total += sys.getsizeof(obj.__dict__)
    return total


assert taille_totale(PointSlot(1, 2)) < taille_totale(Point(1, 2))


print("Toutes les solutions passent ✅")
