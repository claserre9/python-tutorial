"""
Solutions — Chapitre 9
"""
from itertools import count, islice, groupby, pairwise, batched
from functools import cache, partial, reduce


# 9.1 — Range
class Range:
    def __init__(self, start, stop, step=1):
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if (self.step > 0 and self.current >= self.stop) or \
           (self.step < 0 and self.current <= self.stop):
            raise StopIteration
        v = self.current
        self.current += self.step
        return v


assert list(Range(0, 5)) == [0, 1, 2, 3, 4]
assert list(Range(10, 0, -2)) == [10, 8, 6, 4, 2]


# 9.2 — pairs_jusqu_a
def pairs_jusqu_a(n):
    for i in range(n):
        if i % 2 == 0:
            yield i


assert list(pairs_jusqu_a(10)) == [0, 2, 4, 6, 8]


# 9.3 — Pipeline lazy
total = sum(x ** 2 for x in islice(count(), 1000) if x % 3 == 0)
assert total == sum(x ** 2 for x in range(1000) if x % 3 == 0)


# 9.4 — pairwise
def diffs(nombres):
    for a, b in pairwise(nombres):
        yield b - a


assert list(diffs([1, 3, 6, 10])) == [2, 3, 4]


# 9.5 — batched
def par_lots(iterable, n):
    return [list(lot) for lot in batched(iterable, n)]


assert par_lots(range(10), 3) == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]


# 9.6 — groupby (avec tri préalable)
users = [
    {"nom": "Alice",   "pays": "FR"},
    {"nom": "Bob",     "pays": "US"},
    {"nom": "Carol",   "pays": "FR"},
    {"nom": "Dan",     "pays": "US"},
    {"nom": "Eve",     "pays": "FR"},
]

users_tries = sorted(users, key=lambda u: u["pays"])
grouped = {
    pays: [u["nom"] for u in groupe]
    for pays, groupe in groupby(users_tries, key=lambda u: u["pays"])
}
assert grouped == {"FR": ["Alice", "Carol", "Eve"], "US": ["Bob", "Dan"]}


# 9.7 — fib caché
@cache
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


assert fib(10) == 55
assert fib(100) == 354224848179261915075


# 9.8 — partial
def racine(n: int, x: float) -> float:
    return x ** (1 / n)


racine_cubique = partial(racine, 3)
assert abs(racine_cubique(27) - 3) < 1e-9


# 9.9 — Reduce
def produit(nombres):
    return reduce(lambda a, b: a * b, nombres, 1)


assert produit([1, 2, 3, 4]) == 24
assert produit([]) == 1


print("Toutes les solutions passent ✅")
