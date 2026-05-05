"""
Solutions — Chapitre 5
"""
from collections import Counter, defaultdict, deque


# 5.1 — Réponses
# a) deque(maxlen=100)       — buffer circulaire en O(1)
# b) set                     — test d'appartenance O(1)
# c) dict                    — association clé/valeur
# d) tuple                   — immuable et hashable
# e) deque                   — append/popleft O(1)
# f) list + sort(key=...)    — on a besoin d'ordonner, list est OK


# 5.2 — Compréhensions
carres_pairs = [x ** 2 for x in range(21) if x % 2 == 0]
assert carres_pairs == [0, 4, 16, 36, 64, 100, 144, 196, 256, 324, 400]

mot = "hello"
occurrences = {c: mot.count(c) for c in set(mot)}
assert occurrences == {"h": 1, "e": 1, "l": 2, "o": 1}

fichiers = ["main.py", "test.py", "README.md", "setup.cfg", "utils.py"]
extensions = {f.rsplit(".", 1)[-1] for f in fichiers}
assert extensions == {"py", "md", "cfg"}


# 5.3 — defaultdict
noms = ["Alice", "Bob", "Arnaud", "Claire", "Charles", "Alex", "Béatrice"]
grouped = defaultdict(list)
for n in noms:
    grouped[n[0]].append(n)
grouped = dict(grouped)

assert grouped == {
    "A": ["Alice", "Arnaud", "Alex"],
    "B": ["Bob", "Béatrice"],
    "C": ["Claire", "Charles"],
}


# 5.4 — Counter
texte = (
    "Python est un langage puissant. Python est lisible. "
    "Python est polyvalent. Java est verbeux. Python gagne."
)
mots = [m.strip(".").lower() for m in texte.split()]
top3 = Counter(mots).most_common(3)
assert top3[0] == ("python", 4)
assert top3[1] == ("est", 4)
assert len(top3) == 3


# 5.5 — Deque
def traiter_flux(evenements: list) -> int:
    file = deque(evenements)
    n = 0
    while file:
        file.popleft()
        n += 1
    return n


assert traiter_flux(list(range(1000))) == 1000


# 5.6 — Unpacking
a, b = 1, 2
a, b = b, a
assert (a, b) == (2, 1)

donnees = [10, 20, 30, 40, 50]
premier, *milieu, dernier = donnees
assert premier == 10
assert milieu == [20, 30, 40]
assert dernier == 50


# 5.7 — Hashabilité
# hashable : 42, "hello", (1,2,3), frozenset([1,2])
# NON hashable : [1,2,3], {"a":1}, (1, [2,3])  (tuple contenant un élément non hashable)


# 5.8 — Tri composé
users = [
    {"nom": "Bob",    "score": 85},
    {"nom": "Alice",  "score": 90},
    {"nom": "Carol",  "score": 85},
    {"nom": "Dan",    "score": 90},
]

# Astuce : on négate le score pour trier en décroissant, puis nom croissant.
trie = sorted(users, key=lambda u: (-u["score"], u["nom"]))
assert [u["nom"] for u in trie] == ["Alice", "Dan", "Bob", "Carol"]


print("Toutes les solutions passent ✅")
