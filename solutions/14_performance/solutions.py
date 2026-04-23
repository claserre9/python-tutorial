"""
Solutions — Chapitre 14
"""
import gc
import sys
import weakref
from timeit import timeit


# 14.1-14.2 : voir exercices.py — pas de code à produire.


# 14.3 — slots
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


assert taille_totale(PointSlot(1, 2)) < taille_totale(Point(1, 2))


# 14.4 — weakref
class Big: pass
obj = Big()
ref = weakref.ref(obj)
assert ref() is obj
del obj
gc.collect()
assert ref() is None


# 14.5 — WeakValueDictionary
cache = weakref.WeakValueDictionary()

class Ressource:
    def __init__(self, id): self.id = id


r = Ressource("a")
cache["a"] = r
assert cache["a"] is r
del r
gc.collect()
assert "a" not in cache


# 14.6 — optimisation : forme fermée + built-in
def somme_lente(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total


# Option 1 : formule fermée (la plus rapide, mais change l'algo)
#   Σ i² pour i=0..n-1 = (n-1) * n * (2n-1) / 6
def somme_rapide(n: int) -> int:
    # Laisse Python appeler le calcul C de sum + multiplication
    return sum(i * i for i in range(n))
    # Variante encore plus rapide (formule) :
    # return (n - 1) * n * (2 * n - 1) // 6


n = 100_000
t_lent = timeit(lambda: somme_lente(n), number=10)
t_rapide = timeit(lambda: somme_rapide(n), number=10)

assert somme_rapide(n) == somme_lente(n)
# Le gain exact dépend de la machine, mais sum() avec un generator
# est nettement plus rapide que l'accumulation Python pure.
print(f"ratio : {t_lent/t_rapide:.1f}x")


print("Toutes les solutions passent ✅")
