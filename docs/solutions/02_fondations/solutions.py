"""
Solutions — Chapitre 2
"""
import copy
from decimal import Decimal


# =============================================================================
# 2.1 — Identité vs égalité
# =============================================================================
a = [1, 2, 3]
b = [1, 2, 3]
assert a == b        # mêmes valeurs
assert a is not b    # objets distincts en mémoire


# =============================================================================
# 2.2 — Aliasing
# =============================================================================
# x et y pointent vers LE MÊME objet : toute modif de l'un se voit sur l'autre.
# z est une copie : modif indépendante.
#
# x = [1, 2, 3]
# y = x          -> y is x  ✅
# y.append(4)    -> x == [1, 2, 3, 4], y == [1, 2, 3, 4]
#
# z = x.copy()   -> z == x mais z is not x
# z.append(5)    -> x == [1, 2, 3, 4] (inchangé), z == [1, 2, 3, 4, 5]


# =============================================================================
# 2.3 — Défaut mutable
# =============================================================================
def ajoute_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


assert ajoute_tag("python") == ["python"]
assert ajoute_tag("web") == ["web"]


# =============================================================================
# 2.4 — Précision flottante
# =============================================================================
# Les flottants IEEE 754 ne peuvent pas représenter 0.1 exactement.
# 0.1 + 0.2 donne 0.30000000000000004.
# Decimal manipule des nombres en base 10 avec une précision arbitraire.

resultat = Decimal("0.1") + Decimal("0.2")
assert resultat == Decimal("0.3")


# =============================================================================
# 2.5 — f-strings avancées
# =============================================================================
prix = 1234.5678

# Format français : espace pour les milliers, virgule pour les décimales.
# On formate d'abord en US puis on échange les séparateurs.
s1 = f"Prix : {prix:,.2f} €".replace(",", " ").replace(".", ",")

pi = 3.14159
s2 = f"pi ≈ {pi:.2f}"

age = 30
s3 = f"{age=}"

assert s1 == "Prix : 1 234,57 €"
assert s2 == "pi ≈ 3.14"
assert s3 == "age=30"


# =============================================================================
# 2.6 — Truthiness
# =============================================================================
# Falsy : 0, 0.0, "", [], {}, None, False
# Truthy : " " (string non vide), [0] (liste non vide même si contient falsy),
#          {"a":1}, "False" (string non vide, la valeur du contenu n'importe pas)


# =============================================================================
# 2.7 — type() vs isinstance()
# =============================================================================
# Astuce : utiliser type(x) is int force l'égalité EXACTE (pas de sous-classe).
# isinstance(x, int) serait True pour bool aussi (car bool hérite d'int).

def est_nombre_entier(x) -> bool:
    return type(x) is int


assert est_nombre_entier(42) is True
assert est_nombre_entier(True) is False
assert est_nombre_entier(3.14) is False
assert est_nombre_entier("42") is False

# Variante équivalente plus explicite :
# return isinstance(x, int) and not isinstance(x, bool)


# =============================================================================
# 2.8 — Copie profonde
# =============================================================================
matrice = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
copie = copy.deepcopy(matrice)

copie[0][0] = 999
assert matrice[0][0] == 1


print("Toutes les solutions passent ✅")
