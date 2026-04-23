"""
Solutions — Chapitre 4
"""
from collections.abc import Callable


# 4.1 — Signature / et *
def envoyer_email(destinataire, /, sujet, *, corps, **headers):
    return {
        "destinataire": destinataire,
        "sujet": sujet,
        "corps": corps,
        "headers": headers,
    }


assert envoyer_email(
    "alice@example.com", "Hello",
    corps="Salut !",
    priority="high", reply_to="bob@example.com",
) == {
    "destinataire": "alice@example.com",
    "sujet": "Hello",
    "corps": "Salut !",
    "headers": {"priority": "high", "reply_to": "bob@example.com"},
}


# 4.2 — Unpacking / relais
def log_appel(fonc, *args, **kwargs):
    return fonc(*args, **kwargs)


def additionner(a, b, c=0):
    return a + b + c


assert log_appel(additionner, 1, 2) == 3
assert log_appel(additionner, 1, 2, c=10) == 13


# 4.3 — Closures
def compteur(start: int = 0) -> Callable[[], int]:
    n = start
    def incrementer():
        nonlocal n
        n += 1
        return n
    return incrementer


c = compteur()
assert c() == 1
assert c() == 2
c2 = compteur(start=10)
assert c2() == 11
assert c() == 3    # c et c2 ont leur propre n


# 4.4 — Capture tardive
# Le piège : toutes les lambdas capturent la même variable i, qui vaut 4 à la
# fin de la boucle. Solution : utiliser un argument par défaut pour capturer
# la VALEUR au moment de la création de la lambda.

def fabrique_correcte():
    return [lambda i=i: i for i in range(5)]


fonctions = fabrique_correcte()
assert [f() for f in fonctions] == [0, 1, 2, 3, 4]


# 4.5 — Ordre supérieur
def applique_n_fois(fonc, n, valeur):
    for _ in range(n):
        valeur = fonc(valeur)
    return valeur


assert applique_n_fois(lambda x: x * 2, 3, 1) == 8


# 4.6 — Mémoïsation
def memoize(fonc):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = fonc(*args)
        return cache[args]
    return wrapper


appels = 0

@memoize
def carre(x):
    global appels
    appels += 1
    return x * x


carre(5); carre(5); carre(5)
assert appels == 1
carre(3)
assert appels == 2


# 4.7 — Scope : prédictions
# print(x) dans g : 30 (local à g)
# print(x) dans f : 20 (local à f, g a son propre x, pas de nonlocal)
# print(x) global : 10 (inchangé, jamais de global dans f)


# 4.8 — Main guard
# Le code du module s'exécute AUSSI à l'import. Si un autre fichier fait
# `import calcul`, le print() est déclenché -> effet de bord indésirable.
#
# Version correcte :
#
#   def carre(x):
#       return x * x
#
#   if __name__ == "__main__":
#       print(carre(5))


print("Toutes les solutions passent ✅")
