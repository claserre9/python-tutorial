"""
Exercices — Chapitre 14 : Performance
"""
import gc
import sys
import time
import weakref
from timeit import timeit


# =============================================================================
# 14.1 — timeit : comparer deux versions
# =============================================================================
# Comparez `sum(x*x for x in range(1000))` (generator) vs `sum([x*x for x in range(1000)])` (list).
# Affichez le temps des deux, et dites laquelle gagne (en commentaire).

t_gen = timeit("sum(x*x for x in range(1000))", number=10_000)
t_list = timeit("sum([x*x for x in range(1000)])", number=10_000)
print(f"generator: {t_gen:.3f}s  |  list: {t_list:.3f}s")

# Réponse : sur petit volume, la list gagne souvent (allocation unique bulk).
# Sur gros volume (10^7+), le generator gagne (pas de mémoire intermédiaire).


# =============================================================================
# 14.2 — set vs list pour l'appartenance
# =============================================================================
# Mesurez le temps de 10000 tests d'appartenance dans une liste de 10000 éléments
# vs un set de 10000 éléments.
# Le set doit être BEAUCOUP plus rapide.

taille = 10_000
cherches = list(range(taille))

ma_liste = list(range(taille))
mon_set = set(range(taille))

t_list = timeit(lambda: all(x in ma_liste for x in cherches), number=1)
t_set = timeit(lambda: all(x in mon_set for x in cherches), number=1)
print(f"list: {t_list:.3f}s  |  set: {t_set:.3f}s")
assert t_set < t_list / 100, "set devrait être 100x+ plus rapide"


# =============================================================================
# 14.3 — __slots__ : mesurer le gain
# =============================================================================
# Créez 100_000 instances de Point et PointSlot.
# Mesurez la taille mémoire totale avec sys.getsizeof + __dict__ si applicable.

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


class PointSlot:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y


def taille_totale(obj):
    t = sys.getsizeof(obj)
    if hasattr(obj, "__dict__"):
        t += sys.getsizeof(obj.__dict__)
    return t


p = Point(1, 2)
ps = PointSlot(1, 2)
print(f"Point: {taille_totale(p)} octets  |  PointSlot: {taille_totale(ps)} octets")
assert taille_totale(ps) < taille_totale(p)


# =============================================================================
# 14.4 — weakref
# =============================================================================
# Montrez que la destruction de `obj` invalide bien le weakref.

class Big:
    pass


obj = Big()
ref = weakref.ref(obj)

assert ref() is obj       # ref valide tant que obj existe
del obj
gc.collect()
assert ref() is None      # ref invalidée


# =============================================================================
# 14.5 — WeakValueDictionary
# =============================================================================
# Un cache qui disparait automatiquement quand ses valeurs ne sont plus référencées.

cache = weakref.WeakValueDictionary()

class Ressource:
    def __init__(self, id): self.id = id


r = Ressource("a")
cache["a"] = r
assert cache["a"] is r

del r
gc.collect()
assert "a" not in cache     # l'entrée a disparu


# =============================================================================
# 14.6 — Optimisation d'une boucle chaude
# =============================================================================
# La fonction ci-dessous est lente. Proposez une version ACCELEREE en utilisant
# des primitives adaptées. Cible : au moins 2x plus rapide pour n=100_000.

def somme_lente(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total


def somme_rapide(n: int) -> int:
    ...  # TODO


n = 100_000
t_lent = timeit(lambda: somme_lente(n), number=10)
t_rapide = timeit(lambda: somme_rapide(n), number=10)

print(f"lent: {t_lent:.3f}s  |  rapide: {t_rapide:.3f}s")
assert somme_rapide(n) == somme_lente(n)
assert t_rapide < t_lent / 2, f"Attendu 2x+ plus rapide, obtenu ratio={t_lent/t_rapide:.1f}x"


if __name__ == "__main__":
    print("Tous les tests passent ✅")
