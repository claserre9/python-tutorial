"""
Exercices — Chapitre 2 : Modèle objet & types primitifs

Ouvrez ce fichier, complétez chaque exercice, exécutez-le.
Les `assert` doivent passer sans erreur.
"""

# =============================================================================
# 2.1 — Identité vs égalité
# =============================================================================
# Créez deux listes avec le même contenu. Vérifiez qu'elles sont ÉGALES
# mais pas IDENTIQUES.

a = ...  # TODO
b = ...  # TODO

assert a == b, "les listes doivent être égales"
assert a is not b, "les listes doivent être des objets distincts"


# =============================================================================
# 2.2 — Comprendre l'aliasing
# =============================================================================
# Avant d'exécuter, prédisez ce que va afficher chaque print.
# Puis exécutez et expliquez les résultats dans un commentaire.

x = [1, 2, 3]
y = x
y.append(4)
# print(x) affiche quoi ? ->
# print(y) affiche quoi ? ->
# x is y ? ->

z = x.copy()
z.append(5)
# print(x) affiche quoi ? ->
# print(z) affiche quoi ? ->
# x is z ? ->


# =============================================================================
# 2.3 — Le bug du défaut mutable
# =============================================================================
# La fonction ci-dessous a le bug classique. Corrigez-la pour que chaque
# appel parte d'une liste vide.

def ajoute_tag(tag, tags=[]):  # ❌ à corriger
    tags.append(tag)
    return tags


# Après correction :
assert ajoute_tag("python") == ["python"]
assert ajoute_tag("web") == ["web"]  # pas ["python", "web"] !


# =============================================================================
# 2.4 — Précision flottante
# =============================================================================
# Montrez que 0.1 + 0.2 != 0.3 en Python.
# Puis, utilisez le module `decimal` pour faire un calcul EXACT qui vaut 0.3.

assert 0.1 + 0.2 != 0.3  # comprendre pourquoi

from decimal import Decimal
resultat = ...  # TODO: calculer Decimal("0.1") + Decimal("0.2")
assert resultat == Decimal("0.3")


# =============================================================================
# 2.5 — f-strings avancées
# =============================================================================
# Construisez, avec une SEULE f-string chacune, les chaînes attendues.

prix = 1234.5678
# Attendu : "Prix : 1 234,57 €"
# Indice : format {:,.2f} puis remplacer . et , pour le style français
s1 = ...  # TODO

# Attendu : "pi ≈ 3.14"
pi = 3.14159
s2 = ...  # TODO

# Attendu : "age=30"  (utilisez la syntaxe de debug f"{var=}")
age = 30
s3 = ...  # TODO

assert s1 == "Prix : 1 234,57 €"
assert s2 == "pi ≈ 3.14"
assert s3 == "age=30"


# =============================================================================
# 2.6 — Truthiness
# =============================================================================
# Pour chaque valeur, dites si elle est truthy ou falsy SANS l'exécuter,
# puis vérifiez avec bool().

valeurs = [0, 0.0, "", " ", [], [0], {}, {"a": 1}, None, False, "False"]
# Votre prédiction :
# - 0       : falsy
# - 0.0     : falsy
# - ""      : falsy
# - " "     : ?
# - []      : ?
# - [0]     : ?
# - {}      : ?
# - {"a":1} : ?
# - None    : ?
# - False   : ?
# - "False" : ?

for v in valeurs:
    print(f"{v!r:10} -> {bool(v)}")


# =============================================================================
# 2.7 — type() vs isinstance()
# =============================================================================
# bool est une sous-classe de int. Écrivez une fonction `est_nombre_entier`
# qui retourne True pour les int MAIS False pour les bool.

def est_nombre_entier(x) -> bool:
    ...  # TODO


assert est_nombre_entier(42) is True
assert est_nombre_entier(True) is False       # piège !
assert est_nombre_entier(3.14) is False
assert est_nombre_entier("42") is False


# =============================================================================
# 2.8 — Copie profonde
# =============================================================================
# matrice est une liste de listes. Faites-en une copie totalement indépendante.

matrice = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
copie = ...  # TODO

copie[0][0] = 999
assert matrice[0][0] == 1, "la matrice originale doit être intacte"


if __name__ == "__main__":
    print("Tous les tests passent ✅")
