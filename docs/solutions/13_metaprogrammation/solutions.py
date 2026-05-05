"""
Solutions — Chapitre 13
"""
import inspect
from typing import get_type_hints


# 13.1 — type() dynamique
Animal = type("Animal", (), {
    "espece": "animal",
    "crier": lambda self: f"{self.espece} crie",
})

a = Animal()
a.espece = "chat"
assert a.crier() == "chat crie"


# 13.2 — setattr dynamique
class User:
    pass


donnees = {"id": 1, "nom": "Alice", "email": "a@a.com"}
user = User()
for k, v in donnees.items():
    setattr(user, k, v)

assert user.nom == "Alice"


# 13.3 — params_requis
def params_requis(fonc) -> list[str]:
    sig = inspect.signature(fonc)
    return [
        name for name, p in sig.parameters.items()
        if p.default is inspect.Parameter.empty
        and p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]


def f(a, b, c=3, d=4): ...
def g(x, *, y, z=0): ...

assert params_requis(f) == ["a", "b"]
assert params_requis(g) == ["x", "y"]


# 13.4 — get_type_hints
class Noeud:
    valeur: int
    suivant: "Noeud | None"
    nom: str


def champs_de_type(cls, t) -> list[str]:
    hints = get_type_hints(cls)
    return [name for name, ht in hints.items() if ht is t]


assert champs_de_type(Noeud, int) == ["valeur"]
assert champs_de_type(Noeud, str) == ["nom"]


# 13.5 — __init_subclass__
class Plugin:
    REGISTRY: dict[str, type] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.REGISTRY[cls.__name__] = cls


class A(Plugin): pass
class B(Plugin): pass

assert Plugin.REGISTRY["A"] is A
assert Plugin.REGISTRY["B"] is B


# 13.6 — Tagged
class Tagged:
    def __init_subclass__(cls, *, tag: str, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.tag = tag


class Foo(Tagged, tag="foo"): pass
class Bar(Tagged, tag="bar"): pass

assert Foo.tag == "foo"
assert Bar.tag == "bar"


# 13.7 — Proxy
class Proxy:
    def __init__(self, target):
        # ASTUCE : utiliser object.__setattr__ pour éviter une récursion
        # via un éventuel __setattr__ custom.
        object.__setattr__(self, "_target", target)

    def __getattr__(self, name):
        # __getattr__ est appelé seulement si l'attribut N'EXISTE PAS
        # dans __dict__ ou sur la classe. Donc _target y échappe.
        return getattr(self._target, name)


p = Proxy([1, 2, 3])
assert p.count(2) == 1
assert p.index(3) == 2


print("Toutes les solutions passent ✅")
