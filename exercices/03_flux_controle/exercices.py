"""
Exercices — Chapitre 3 : Flux de contrôle
"""

# =============================================================================
# 3.1 — Chaînage de comparaisons
# =============================================================================
# Écrivez une fonction `est_age_valide(age)` qui retourne True si age est
# entre 0 et 120 inclus, en utilisant UNE SEULE comparaison chaînée.

def est_age_valide(age: int) -> bool:
    ...  # TODO


assert est_age_valide(0) is True
assert est_age_valide(120) is True
assert est_age_valide(-1) is False
assert est_age_valide(121) is False


# =============================================================================
# 3.2 — Court-circuit et défaut
# =============================================================================
# Écrivez une fonction `nom_affichable(nom)` qui retourne le nom si non vide,
# sinon "Anonyme". Utilisez l'opérateur `or`.

def nom_affichable(nom: str) -> str:
    ...  # TODO une seule ligne avec `or`


assert nom_affichable("Alice") == "Alice"
assert nom_affichable("") == "Anonyme"
assert nom_affichable(None) == "Anonyme"


# =============================================================================
# 3.3 — for/else
# =============================================================================
# Écrivez `tous_positifs(nombres)` qui affiche "OK" si tous les nombres sont >= 0
# et "Négatif trouvé" dès qu'il en détecte un.
# Utilisez la clause else d'un for.

def tous_positifs(nombres):
    ...  # TODO


# Doit afficher "OK"
tous_positifs([1, 2, 3])
# Doit afficher "Négatif trouvé"
tous_positifs([1, -2, 3])


# =============================================================================
# 3.4 — FizzBuzz
# =============================================================================
# L'exercice classique. Pour i de 1 à 30 :
# - si i multiple de 3 ET 5 : afficher "FizzBuzz"
# - si i multiple de 3 : "Fizz"
# - si i multiple de 5 : "Buzz"
# - sinon : i
# Bonus : écrivez-le en UNE LIGNE par itération avec un ternaire.

# TODO


# =============================================================================
# 3.5 — Walrus
# =============================================================================
# Lisez les entrées de l'utilisateur jusqu'à ce qu'il tape "quit".
# Utilisez l'opérateur walrus pour condenser la lecture et la condition
# en une seule ligne while.
#
# Pour tester sans input interactif, utilisez la liste ci-dessous via iter().

entrees = iter(["bonjour", "python", "quit", "jamais"])

def lire():
    return next(entrees, "quit")

# TODO : boucle while avec walrus qui affiche les entrées sauf "quit"


# =============================================================================
# 3.6 — Pattern matching : déstructuration de séquence
# =============================================================================
# Écrivez `analyse(cmd)` qui prend une list[str] et retourne :
# - "vide" si la liste est vide
# - f"simple: {action}" si un seul élément
# - f"{action} -> {cible}" si deux éléments
# - f"{action} sur {n} cibles" si plus (avec n = nb de cibles)
# Utilisez match/case avec déstructuration.

def analyse(cmd: list[str]) -> str:
    ...  # TODO


assert analyse([]) == "vide"
assert analyse(["start"]) == "simple: start"
assert analyse(["copy", "file.txt"]) == "copy -> file.txt"
assert analyse(["delete", "a", "b", "c"]) == "delete sur 3 cibles"


# =============================================================================
# 3.7 — Pattern matching : dict et classes
# =============================================================================
# On reçoit des événements sous forme de dict. Implémentez `decrire(event)` :
# - {"type": "click", "x": X, "y": Y}       -> f"clic ({X},{Y})"
# - {"type": "key", "key": K}               -> f"touche {K}"
# - {"type": "scroll", "delta": D} si D > 0 -> "scroll up"
# - {"type": "scroll", "delta": D} si D < 0 -> "scroll down"
# - autre                                    -> "inconnu"

def decrire(event: dict) -> str:
    ...  # TODO


assert decrire({"type": "click", "x": 10, "y": 20}) == "clic (10,20)"
assert decrire({"type": "key", "key": "a"}) == "touche a"
assert decrire({"type": "scroll", "delta": 5}) == "scroll up"
assert decrire({"type": "scroll", "delta": -3}) == "scroll down"
assert decrire({"type": "hover"}) == "inconnu"


# =============================================================================
# 3.8 — Le piège du match
# =============================================================================
# Le code suivant NE fonctionne PAS comme prévu. Expliquez pourquoi dans un
# commentaire, puis corrigez-le pour qu'il compare bien MAX à x.

MAX = 100

def ancien_check(x):
    match x:
        case MAX:         # ❌ ce n'est PAS une comparaison !
            return "max atteint"
        case _:
            return "autre"

# TODO : ré-implémentez `check` qui compare correctement x à MAX.

def check(x) -> str:
    ...  # TODO


assert check(100) == "max atteint"
assert check(50) == "autre"
assert check(200) == "autre"


if __name__ == "__main__":
    print("Tous les tests passent ✅")
