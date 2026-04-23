"""
Exercices — Chapitre 11 : Décorateurs & descripteurs
"""
import time
from functools import wraps
from typing import Callable, ParamSpec, TypeVar


# =============================================================================
# 11.1 — Décorateur basique avec wraps
# =============================================================================
# Écrivez @double qui appelle la fonction 2 fois et retourne (r1, r2).
# Préservez __name__ avec wraps.

def double(fn):
    ...  # TODO


@double
def dit(msg):
    """Dit le message."""
    return msg.upper()


r = dit("hello")
assert r == ("HELLO", "HELLO")
assert dit.__name__ == "dit"
assert "Dit le message" in dit.__doc__


# =============================================================================
# 11.2 — Décorateur paramétré : @retry
# =============================================================================
# Écrivez @retry(times=N) qui retente la fonction si elle lève une exception.
# Après N échecs, la dernière exception doit remonter.

def retry(times: int = 3):
    ...  # TODO


compteur = [0]

@retry(times=3)
def flaky():
    compteur[0] += 1
    if compteur[0] < 3:
        raise ValueError("pas encore")
    return "ok"


assert flaky() == "ok"
assert compteur[0] == 3

compteur[0] = 0
@retry(times=2)
def toujours_casse():
    compteur[0] += 1
    raise ValueError("boom")


import pytest
with pytest.raises(ValueError):
    toujours_casse()
assert compteur[0] == 2


# =============================================================================
# 11.3 — Décorateur typé avec ParamSpec
# =============================================================================
# Complétez le typage pour que mypy voie que `additionner` reste
# Callable[[int, int], int] après décoration.

P = ParamSpec("P")
R = TypeVar("R")


def timed(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        print(f"{fn.__name__}: {elapsed:.4f}s")
        return result
    return wrapper


@timed
def additionner(a: int, b: int) -> int:
    return a + b


assert additionner(3, 4) == 7


# =============================================================================
# 11.4 — Décorateur de classe : @register
# =============================================================================
# Écrivez @register qui ajoute la classe dans un dict REGISTRY indexé par __name__.

REGISTRY: dict[str, type] = {}


def register(cls):
    ...  # TODO


@register
class PluginA: ...


@register
class PluginB: ...


assert "PluginA" in REGISTRY
assert "PluginB" in REGISTRY
assert REGISTRY["PluginA"] is PluginA


# =============================================================================
# 11.5 — Empilement : l'ordre compte
# =============================================================================
# Analysez le code ci-dessous SANS l'exécuter. Qu'affiche f(5) ?

def mul2(fn):
    @wraps(fn)
    def wrapper(x):
        return fn(x) * 2
    return wrapper

def add10(fn):
    @wraps(fn)
    def wrapper(x):
        return fn(x) + 10
    return wrapper


@add10
@mul2
def f(x):
    return x


# f(5) : quelle valeur ?
# Prédisez AVANT de vérifier.
# Réponse dans un commentaire, puis vérifiez :
assert f(5) == ...    # TODO : remplacer par la valeur


# =============================================================================
# 11.6 — Descripteur simple : TypedField
# =============================================================================
# Implémentez TypedField qui impose un type à un attribut.
# Doit utiliser __set_name__ pour connaître le nom de l'attribut.

class TypedField:
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __set_name__(self, owner, name):
        ...  # TODO

    def __get__(self, instance, owner):
        ...  # TODO

    def __set__(self, instance, value):
        ...  # TODO : vérifier isinstance, sinon TypeError


class Personne:
    nom = TypedField(str)
    age = TypedField(int)


p = Personne()
p.nom = "Alice"
p.age = 30
assert p.nom == "Alice"
assert p.age == 30

with pytest.raises(TypeError):
    p.age = "trente"


# =============================================================================
# 11.7 — Descripteur : lazy_property
# =============================================================================
# Implémentez lazy_property : calcule une seule fois, cache ensuite dans
# instance.__dict__.

class lazy_property:
    def __init__(self, fn):
        self.fn = fn

    def __set_name__(self, owner, name):
        ...  # TODO

    def __get__(self, instance, owner):
        ...  # TODO


appels = [0]

class Rapport:
    def __init__(self, data):
        self.data = data

    @lazy_property
    def stats(self):
        appels[0] += 1
        return sum(self.data)


r = Rapport([1, 2, 3, 4])
assert r.stats == 10
assert r.stats == 10
assert r.stats == 10
assert appels[0] == 1     # UN seul calcul


if __name__ == "__main__":
    print("Tous les tests passent ✅")
