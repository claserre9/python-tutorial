"""
Exercices — Chapitre 13 : Métaprogrammation & introspection
"""
import inspect
from typing import get_type_hints


# =============================================================================
# 13.1 — Créer une classe avec type()
# =============================================================================
# Créez la classe Animal équivalente à :
#   class Animal:
#       espece = "animal"
#       def crier(self): return f"{self.espece} crie"
# Mais uniquement via type(name, bases, dict).

Animal = ...  # TODO


a = Animal()
a.espece = "chat"
assert a.crier() == "chat crie"


# =============================================================================
# 13.2 — Setattr dynamique
# =============================================================================
# Peuplez les attributs de `user` depuis un dict.

class User:
    pass


donnees = {"id": 1, "nom": "Alice", "email": "a@a.com"}
user = User()

# TODO : setattr pour chaque clé
...

assert user.id == 1
assert user.nom == "Alice"
assert user.email == "a@a.com"


# =============================================================================
# 13.3 — inspect.signature
# =============================================================================
# Écrivez `params_requis(fonc)` qui retourne la liste des noms des paramètres
# SANS valeur par défaut.

def params_requis(fonc) -> list[str]:
    ...  # TODO


def f(a, b, c=3, d=4): ...
def g(x, *, y, z=0): ...

assert params_requis(f) == ["a", "b"]
assert params_requis(g) == ["x", "y"]


# =============================================================================
# 13.4 — get_type_hints et forward refs
# =============================================================================
# Soit la classe ci-dessous. Écrivez `champs_de_type(cls, t)` qui retourne
# les noms des attributs de cls dont le type résolu EST t.

class Noeud:
    valeur: int
    suivant: "Noeud | None"
    nom: str


def champs_de_type(cls, t) -> list[str]:
    ...  # TODO : utiliser get_type_hints


# int : valeur
# str : nom
# "Noeud | None" : suivant (type union)
assert champs_de_type(Noeud, int) == ["valeur"]
assert champs_de_type(Noeud, str) == ["nom"]


# =============================================================================
# 13.5 — __init_subclass__
# =============================================================================
# Implémentez Plugin de telle sorte que chaque sous-classe soit
# automatiquement enregistrée dans Plugin.REGISTRY (par nom de classe).

class Plugin:
    REGISTRY: dict[str, type] = {}

    def __init_subclass__(cls, **kwargs):
        ...  # TODO


class A(Plugin): pass
class B(Plugin): pass

assert "A" in Plugin.REGISTRY
assert "B" in Plugin.REGISTRY
assert Plugin.REGISTRY["A"] is A


# =============================================================================
# 13.6 — __init_subclass__ avec paramètres
# =============================================================================
# Permettez à l'utilisateur de passer un tag à la création :
#   class X(Tagged, tag="foo"): ...
# Et X.tag doit valoir "foo".

class Tagged:
    def __init_subclass__(cls, *, tag: str, **kwargs):
        ...  # TODO


class Foo(Tagged, tag="foo"): pass
class Bar(Tagged, tag="bar"): pass

assert Foo.tag == "foo"
assert Bar.tag == "bar"


# =============================================================================
# 13.7 — Proxy via __getattr__
# =============================================================================
# Implémentez un Proxy qui délègue tous les attributs manquants à un objet cible.

class Proxy:
    def __init__(self, target):
        ...  # TODO : stocker target dans _target (éviter récursion)

    def __getattr__(self, name):
        ...  # TODO


p = Proxy([1, 2, 3])
assert p.count(2) == 1        # délégué à list.count
assert p.index(3) == 2        # délégué à list.index


if __name__ == "__main__":
    print("Tous les tests passent ✅")
