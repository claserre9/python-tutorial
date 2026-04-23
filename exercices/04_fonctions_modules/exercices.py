"""
Exercices — Chapitre 4 : Fonctions & scope
"""
from collections.abc import Callable


# =============================================================================
# 4.1 — Signature avec / et *
# =============================================================================
# Écrivez `envoyer_email(destinataire, /, sujet, *, corps, **headers)` qui
# retourne un dict contenant toutes les infos.
#
# Contraintes :
# - destinataire est positional-only
# - corps est keyword-only
# - headers capture tout le reste en nommé

def envoyer_email(...):    # TODO
    ...


resultat = envoyer_email(
    "alice@example.com",
    "Hello",
    corps="Salut !",
    priority="high",
    reply_to="bob@example.com",
)
assert resultat == {
    "destinataire": "alice@example.com",
    "sujet": "Hello",
    "corps": "Salut !",
    "headers": {"priority": "high", "reply_to": "bob@example.com"},
}


# =============================================================================
# 4.2 — Unpacking
# =============================================================================
# Utilisez * et ** pour relayer les arguments à la fonction existante.

def log_appel(fonc, *args, **kwargs):
    """Appelle fonc avec les arguments relayés et retourne son résultat."""
    ...  # TODO


def additionner(a, b, c=0):
    return a + b + c


assert log_appel(additionner, 1, 2) == 3
assert log_appel(additionner, 1, 2, c=10) == 13
assert log_appel(additionner, *[4, 5], **{"c": 100}) == 109


# =============================================================================
# 4.3 — Closures
# =============================================================================
# Écrivez `compteur(start=0)` qui retourne une fonction sans argument :
# chaque appel incrémente et retourne la nouvelle valeur.
# Utilisez nonlocal.

def compteur(start: int = 0) -> Callable[[], int]:
    ...  # TODO


c = compteur()
assert c() == 1
assert c() == 2
assert c() == 3

c2 = compteur(start=10)
assert c2() == 11
assert c2() == 12
assert c() == 4    # c et c2 sont indépendants


# =============================================================================
# 4.4 — Piège de la capture tardive
# =============================================================================
# Le code ci-dessous NE marche PAS comme prévu.
# Corrigez la fabrique pour qu'elle capture correctement i.

def fabrique_cassee():
    return [lambda: i for i in range(5)]


def fabrique_correcte():
    ...  # TODO


fonctions = fabrique_correcte()
assert [f() for f in fonctions] == [0, 1, 2, 3, 4]


# =============================================================================
# 4.5 — Fonction d'ordre supérieur
# =============================================================================
# Écrivez `applique_n_fois(fonc, n, valeur)` qui applique fonc n fois à valeur.
# Ex: applique_n_fois(lambda x: x * 2, 3, 1) == 8

def applique_n_fois(fonc: Callable, n: int, valeur):
    ...  # TODO


assert applique_n_fois(lambda x: x * 2, 3, 1) == 8
assert applique_n_fois(lambda x: x + 1, 5, 0) == 5
assert applique_n_fois(str.upper, 1, "hello") == "HELLO"


# =============================================================================
# 4.6 — Mémoïsation manuelle
# =============================================================================
# Écrivez `memoize(fonc)` qui retourne une version de fonc qui cache
# ses résultats. Simple : ne gérer que les appels positionnels hashables.

def memoize(fonc):
    cache = {}
    def wrapper(*args):
        ...  # TODO
    return wrapper


appels = 0

@memoize
def carre(x):
    global appels
    appels += 1
    return x * x


assert carre(5) == 25
assert carre(5) == 25
assert carre(5) == 25
assert appels == 1   # ne doit être appelé qu'une fois pour le même argument

assert carre(3) == 9
assert appels == 2


# =============================================================================
# 4.7 — Scope : prédire le résultat
# =============================================================================
# Sans exécuter, dites ce que chaque print affiche. Justifiez avec LEGB.

x = 10

def f():
    x = 20
    def g():
        x = 30
        print(x)    # ?
    g()
    print(x)        # ?

f()
print(x)            # ?


# =============================================================================
# 4.8 — Modules : main guard
# =============================================================================
# Expliquez en commentaire pourquoi le code ci-dessous est une mauvaise pratique,
# puis proposez une version corrigée.

# calcul.py (VERSION MAUVAISE)
def carre(x):
    return x * x

print(carre(5))   # ← problème : s'exécute à l'import

# TODO : ré-écrivez dans un commentaire la version correcte.


if __name__ == "__main__":
    print("Tous les tests passent ✅")
