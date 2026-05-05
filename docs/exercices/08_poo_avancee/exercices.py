"""
Exercices — Chapitre 8 : POO avancée
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


# =============================================================================
# 8.1 — MRO et super() coopératif
# =============================================================================
# Complétez les classes pour que D() affiche dans l'ordre "D B C A".
# Utilisez super() partout (même dans A).

class A:
    def __init__(self):
        ...  # TODO

class B(A):
    def __init__(self):
        ...  # TODO

class C(A):
    def __init__(self):
        ...  # TODO

class D(B, C):
    def __init__(self):
        ...  # TODO


import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    D()
assert buf.getvalue() == "D\nB\nC\nA\n", f"Obtenu : {buf.getvalue()!r}"
assert [c.__name__ for c in D.__mro__] == ["D", "B", "C", "A", "object"]


# =============================================================================
# 8.2 — Classe abstraite Forme
# =============================================================================
# Définissez Forme (ABC) avec aire() et perimetre() abstraites.
# Puis Rectangle et Cercle qui implémentent.

class Forme(ABC):
    ...  # TODO


class Rectangle(Forme):
    ...  # TODO


class Cercle(Forme):
    ...  # TODO


import pytest
with pytest.raises(TypeError):
    Forme()    # impossible d'instancier une classe abstraite

r = Rectangle(3, 4)
assert r.aire() == 12
assert r.perimetre() == 14

from math import pi, isclose
c = Cercle(5)
assert isclose(c.aire(), pi * 25)


# =============================================================================
# 8.3 — Protocol : duck typing typé
# =============================================================================
# Définissez un Protocol `Serialisable` avec une méthode `to_dict() -> dict`.
# Puis deux classes INDÉPENDANTES (pas d'héritage) qui le satisfont.

@runtime_checkable
class Serialisable(Protocol):
    ...  # TODO


class Produit:
    def __init__(self, nom, prix):
        self.nom, self.prix = nom, prix
    # TODO : implémenter to_dict()


class Event:
    def __init__(self, titre):
        self.titre = titre
    # TODO : implémenter to_dict()


def exporter(obj: Serialisable) -> dict:
    return obj.to_dict()


assert exporter(Produit("laptop", 1200)) == {"nom": "laptop", "prix": 1200}
assert exporter(Event("conf")) == {"titre": "conf"}
assert isinstance(Produit("a", 1), Serialisable)


# =============================================================================
# 8.4 — Composition (injection de dépendance)
# =============================================================================
# Définissez une interface Notifier (ABC) avec `envoyer(dest, msg)`.
# Définissez EmailNotifier et FakeNotifier (pour les tests, stocke dans une liste).
# Définissez UserService(notifier) qui appelle notifier.envoyer().

class Notifier(ABC):
    ...  # TODO


class FakeNotifier(Notifier):
    # Stocke chaque envoi dans self.envois
    ...  # TODO


class UserService:
    def __init__(self, notifier: Notifier):
        ...  # TODO

    def bienvenue(self, user_email: str) -> None:
        ...  # TODO : notifier.envoyer(user_email, "Bienvenue !")


fake = FakeNotifier()
svc = UserService(fake)
svc.bienvenue("alice@a.com")
svc.bienvenue("bob@b.com")
assert fake.envois == [("alice@a.com", "Bienvenue !"), ("bob@b.com", "Bienvenue !")]


# =============================================================================
# 8.5 — dataclass kw_only en héritage
# =============================================================================
# Corrigez le code suivant : il doit permettre à Derived d'avoir un champ
# avec défaut, et Base un champ sans défaut.

# Version cassée :
# @dataclass
# class Base:
#     x: int
# @dataclass
# class Derived(Base):
#     y: int = 0

# TODO : ré-écrivez en kw_only

@dataclass(...)    # TODO
class Base:
    x: int


@dataclass(...)    # TODO
class Derived(Base):
    y: int = 0


d = Derived(x=5)
assert d.x == 5 and d.y == 0


# =============================================================================
# 8.6 — Performance : slots
# =============================================================================
# Mesurez l'économie mémoire entre Point (classique) et PointSlot (slots).
# Utilisez sys.getsizeof() sur une instance.

import sys


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


class PointSlot:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y


# Attention : sys.getsizeof() sur une instance ne compte QUE l'objet lui-même,
# pas son __dict__. Pour une comparaison plus juste :
def taille_totale(obj) -> int:
    total = sys.getsizeof(obj)
    if hasattr(obj, "__dict__"):
        total += sys.getsizeof(obj.__dict__)
    return total


classique = taille_totale(Point(1, 2))
avec_slots = taille_totale(PointSlot(1, 2))
print(f"Classique: {classique} octets, Slots: {avec_slots} octets")
assert avec_slots < classique


if __name__ == "__main__":
    print("Tous les tests passent ✅")
