"""
Exercices — Chapitre 9 : Itérateurs, générateurs, fonctionnel
"""
from itertools import chain, islice, groupby, pairwise, batched
from functools import cache, partial, reduce


# =============================================================================
# 9.1 — Itérateur custom
# =============================================================================
# Implémentez une classe Range(start, stop, step=1) qui se comporte comme
# range() : itérable, utilisable dans un for.

class Range:
    ...  # TODO : __init__, __iter__, __next__


assert list(Range(0, 5)) == [0, 1, 2, 3, 4]
assert list(Range(10, 0, -2)) == [10, 8, 6, 4, 2]


# =============================================================================
# 9.2 — Générateur basique
# =============================================================================
# Écrivez un générateur `pairs_jusqu_a(n)` qui yield les nombres pairs de 0 à n (exclu).

def pairs_jusqu_a(n):
    ...  # TODO


assert list(pairs_jusqu_a(10)) == [0, 2, 4, 6, 8]


# =============================================================================
# 9.3 — Pipeline lazy
# =============================================================================
# On a une liste infinie simulée (count). Écrivez une expression qui :
#  - prend les 1000 premiers entiers
#  - garde les multiples de 3
#  - élève au carré
#  - somme le tout
# TOUT en lazy (générateurs), pas de list intermédiaire.

from itertools import count

total = ...  # TODO : une expression utilisant islice, une expr génératrice, sum
assert total == sum(x ** 2 for x in range(1000) if x % 3 == 0)


# =============================================================================
# 9.4 — Fenêtre glissante
# =============================================================================
# Avec itertools.pairwise, calculez la liste des DIFFÉRENCES consécutives.

def diffs(nombres):
    ...  # TODO : utiliser pairwise


assert list(diffs([1, 3, 6, 10])) == [2, 3, 4]


# =============================================================================
# 9.5 — Lots (batched)
# =============================================================================
# Avec itertools.batched (3.12+), divisez une liste en lots de taille n.
# Retournez les lots en tant que listes (pas tuples).

def par_lots(iterable, n):
    ...  # TODO


assert par_lots(range(10), 3) == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]


# =============================================================================
# 9.6 — groupby
# =============================================================================
# On a des utilisateurs avec un pays. Groupez-les par pays.
# ATTENTION : groupby regroupe les éléments CONSÉCUTIFS. Triez d'abord !

users = [
    {"nom": "Alice",   "pays": "FR"},
    {"nom": "Bob",     "pays": "US"},
    {"nom": "Carol",   "pays": "FR"},
    {"nom": "Dan",     "pays": "US"},
    {"nom": "Eve",     "pays": "FR"},
]

grouped = {}   # TODO : {pays: [noms]}
assert grouped == {"FR": ["Alice", "Carol", "Eve"], "US": ["Bob", "Dan"]}


# =============================================================================
# 9.7 — Mémoïsation avec @cache
# =============================================================================
# Implémentez fib(n) de façon récursive NAÏVE mais décorée par @cache.
# Vérifiez que fib(100) est calculé instantanément.

@cache
def fib(n: int) -> int:
    ...  # TODO


assert fib(10) == 55
assert fib(100) == 354224848179261915075


# =============================================================================
# 9.8 — partial : curry
# =============================================================================
# Créez une fonction `racine` qui calcule la racine n-ième de x.
# Puis dérivez `racine_cubique` avec partial.

def racine(n: int, x: float) -> float:
    return x ** (1 / n)


racine_cubique = ...  # TODO : partial

assert abs(racine_cubique(27) - 3) < 1e-9


# =============================================================================
# 9.9 — Reduce
# =============================================================================
# Avec reduce, calculez le produit d'une liste d'entiers.
# (Oui, math.prod existe depuis 3.8 — mais l'exercice est sur reduce.)

def produit(nombres):
    ...  # TODO


assert produit([1, 2, 3, 4]) == 24
assert produit([]) == 1    # indice : utiliser initial=1


if __name__ == "__main__":
    print("Tous les tests passent ✅")
