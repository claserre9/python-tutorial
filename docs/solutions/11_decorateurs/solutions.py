"""
Solutions — Chapitre 11
"""
import time
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

import pytest


# 11.1 — double
def double(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return (fn(*args, **kwargs), fn(*args, **kwargs))
    return wrapper


@double
def dit(msg):
    """Dit le message."""
    return msg.upper()


r = dit("hello")
assert r == ("HELLO", "HELLO")
assert dit.__name__ == "dit"


# 11.2 — retry
def retry(times: int = 3):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for _ in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
            assert last_exc is not None
            raise last_exc
        return wrapper
    return decorator


compteur = [0]

@retry(times=3)
def flaky():
    compteur[0] += 1
    if compteur[0] < 3:
        raise ValueError("pas encore")
    return "ok"


assert flaky() == "ok"
assert compteur[0] == 3


# 11.3 — timed typé (déjà typé dans l'exercice)
P = ParamSpec("P")
R = TypeVar("R")


def timed(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        print(f"{fn.__name__}: {time.perf_counter() - t0:.4f}s")
        return result
    return wrapper


# 11.4 — register
REGISTRY: dict[str, type] = {}

def register(cls):
    REGISTRY[cls.__name__] = cls
    return cls


@register
class PluginA: ...


@register
class PluginB: ...


assert REGISTRY["PluginA"] is PluginA


# 11.5 — Empilement
# @add10 @mul2 → add10(mul2(f))
# f(5) = 5 ; mul2(f)(5) = 10 ; add10(mul2(f))(5) = 20
def mul2(fn):
    @wraps(fn)
    def wrapper(x): return fn(x) * 2
    return wrapper

def add10(fn):
    @wraps(fn)
    def wrapper(x): return fn(x) + 10
    return wrapper

@add10
@mul2
def f(x): return x

assert f(5) == 20


# 11.6 — TypedField
class TypedField:
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name}: attendu {self.expected_type.__name__}")
        instance.__dict__[self.name] = value


class Personne:
    nom = TypedField(str)
    age = TypedField(int)


p = Personne()
p.nom = "Alice"
p.age = 30

with pytest.raises(TypeError):
    p.age = "trente"


# 11.7 — lazy_property
class lazy_property:
    def __init__(self, fn):
        self.fn = fn

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        val = self.fn(instance)
        instance.__dict__[self.name] = val    # masque le descripteur
        return val


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
assert appels[0] == 1


print("Toutes les solutions passent ✅")
