"""
Exercices — Chapitre 5 : Structures de données
"""
from collections import Counter, defaultdict, deque


# =============================================================================
# 5.1 — Choisir la bonne structure
# =============================================================================
# Pour chaque besoin, dites quelle structure utiliser (list/tuple/dict/set/deque).
#
# a) Garder les 100 dernières requêtes HTTP            -> ?
# b) Savoir si un email est déjà enregistré, rapide    -> ?
# c) Associer un user_id à un objet User               -> ?
# d) Coordonnées (x, y) immuables utilisables en clé   -> ?
# e) File d'événements (FIFO, append droite, pop gauche) -> ?
# f) Trier des utilisateurs par date d'inscription     -> ?

# Répondez dans des commentaires ci-dessus.


# =============================================================================
# 5.2 — Compréhensions
# =============================================================================
# Construisez avec UNE compréhension chacune :
#
# a) Liste des carrés des nombres pairs de 0 à 20 inclus
carres_pairs = ...  # TODO
assert carres_pairs == [0, 4, 16, 36, 64, 100, 144, 196, 256, 324, 400]

# b) Dict qui associe chaque lettre du mot "hello" au nombre d'occurrences
#    Utilisez Counter si vous voulez, mais essayez d'abord sans.
occurrences = ...  # TODO
assert occurrences == {"h": 1, "e": 1, "l": 2, "o": 1}

# c) Set des extensions présentes dans la liste de fichiers
fichiers = ["main.py", "test.py", "README.md", "setup.cfg", "utils.py"]
extensions = ...  # TODO (set d'extensions SANS le point : "py", "md", "cfg")
assert extensions == {"py", "md", "cfg"}


# =============================================================================
# 5.3 — Group by avec defaultdict
# =============================================================================
# À partir de la liste ci-dessous, produisez un dict qui GROUPE les noms
# par première lettre. Utilisez defaultdict(list).

noms = ["Alice", "Bob", "Arnaud", "Claire", "Charles", "Alex", "Béatrice"]
grouped = ...  # TODO

assert grouped == {
    "A": ["Alice", "Arnaud", "Alex"],
    "B": ["Bob", "Béatrice"],
    "C": ["Claire", "Charles"],
}


# =============================================================================
# 5.4 — Counter
# =============================================================================
# Trouvez les 3 mots les plus fréquents dans le texte (insensible à la casse).

texte = (
    "Python est un langage puissant. Python est lisible. "
    "Python est polyvalent. Java est verbeux. Python gagne."
)
top3 = ...  # TODO : list[tuple[str, int]]

assert top3[0] == ("python", 4)
assert top3[1] == ("est", 4)
assert len(top3) == 3


# =============================================================================
# 5.5 — Deque vs list : performance
# =============================================================================
# Complétez la fonction pour utiliser la bonne structure (deque) : on traite
# un flux de 100_000 événements, en retirant toujours le plus ancien.

def traiter_flux(evenements: list) -> int:
    """Retire les événements un par un depuis le DÉBUT, retourne le nb traité."""
    file = ...  # TODO : choisir deque(...)
    n = 0
    while file:
        file.popleft()
        n += 1
    return n


assert traiter_flux(list(range(1000))) == 1000


# =============================================================================
# 5.6 — Unpacking
# =============================================================================
# a) Échangez a et b en UNE ligne.
a = 1
b = 2
# TODO
assert (a, b) == (2, 1)

# b) Extraire le premier et le dernier élément, stocker le milieu dans `milieu`.
donnees = [10, 20, 30, 40, 50]
premier, *milieu, dernier = ...  # TODO
assert premier == 10
assert milieu == [20, 30, 40]
assert dernier == 50


# =============================================================================
# 5.7 — Hashabilité
# =============================================================================
# Pour chaque valeur, dites si elle est HASHABLE (donc utilisable en clé/élément
# de set). Confirmez avec hash(...) (lève TypeError si non hashable).

candidats = [
    42,
    "hello",
    (1, 2, 3),
    [1, 2, 3],
    {"a": 1},
    frozenset([1, 2]),
    (1, [2, 3]),       # tuple contenant une liste
]

# TODO : pour chaque, prédisez hashable ou non avant de tester.

for c in candidats:
    try:
        hash(c)
        print(f"{c!r:30} -> hashable")
    except TypeError:
        print(f"{c!r:30} -> NON hashable")


# =============================================================================
# 5.8 — Tri par critère composé
# =============================================================================
# Triez la liste d'utilisateurs par :
#   1) score DÉCROISSANT
#   2) à score égal, nom CROISSANT (alphabétique)

users = [
    {"nom": "Bob",    "score": 85},
    {"nom": "Alice",  "score": 90},
    {"nom": "Carol",  "score": 85},
    {"nom": "Dan",    "score": 90},
]

trie = ...  # TODO

assert [u["nom"] for u in trie] == ["Alice", "Dan", "Bob", "Carol"]


if __name__ == "__main__":
    print("Tous les tests passent ✅")
