"""
Solutions — Chapitre 3
"""

# 3.1 — Chaînage de comparaisons
def est_age_valide(age: int) -> bool:
    return 0 <= age <= 120


assert est_age_valide(0) is True
assert est_age_valide(120) is True
assert est_age_valide(-1) is False
assert est_age_valide(121) is False


# 3.2 — Court-circuit
def nom_affichable(nom) -> str:
    return nom or "Anonyme"


assert nom_affichable("Alice") == "Alice"
assert nom_affichable("") == "Anonyme"
assert nom_affichable(None) == "Anonyme"


# 3.3 — for/else
def tous_positifs(nombres):
    for n in nombres:
        if n < 0:
            print("Négatif trouvé")
            break
    else:
        print("OK")


tous_positifs([1, 2, 3])      # OK
tous_positifs([1, -2, 3])     # Négatif trouvé


# 3.4 — FizzBuzz (version ternaire + logique factorisée)
for i in range(1, 31):
    sortie = (
        "FizzBuzz" if i % 15 == 0
        else "Fizz" if i % 3 == 0
        else "Buzz" if i % 5 == 0
        else i
    )
    print(sortie)


# 3.5 — Walrus
entrees = iter(["bonjour", "python", "quit", "jamais"])

def lire():
    return next(entrees, "quit")

while (mot := lire()) != "quit":
    print(mot)


# 3.6 — Match : séquences
def analyse(cmd: list[str]) -> str:
    match cmd:
        case []:
            return "vide"
        case [action]:
            return f"simple: {action}"
        case [action, cible]:
            return f"{action} -> {cible}"
        case [action, *cibles]:
            return f"{action} sur {len(cibles)} cibles"


assert analyse([]) == "vide"
assert analyse(["start"]) == "simple: start"
assert analyse(["copy", "file.txt"]) == "copy -> file.txt"
assert analyse(["delete", "a", "b", "c"]) == "delete sur 3 cibles"


# 3.7 — Match : dicts avec gardes
def decrire(event: dict) -> str:
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"clic ({x},{y})"
        case {"type": "key", "key": k}:
            return f"touche {k}"
        case {"type": "scroll", "delta": d} if d > 0:
            return "scroll up"
        case {"type": "scroll", "delta": d} if d < 0:
            return "scroll down"
        case _:
            return "inconnu"


assert decrire({"type": "click", "x": 10, "y": 20}) == "clic (10,20)"
assert decrire({"type": "key", "key": "a"}) == "touche a"
assert decrire({"type": "scroll", "delta": 5}) == "scroll up"
assert decrire({"type": "scroll", "delta": -3}) == "scroll down"
assert decrire({"type": "hover"}) == "inconnu"


# 3.8 — Piège du match
# EXPLICATION : un NOM non qualifié dans un case est une LIAISON (capture),
# pas une comparaison. `case MAX:` lie x à une variable nommée MAX,
# ce qui correspond à tout. Il faut qualifier (ex. MODULE.MAX) ou utiliser
# un garde. Ici on opte pour le garde, plus clair.

MAX = 100

def check(x) -> str:
    match x:
        case n if n == MAX:
            return "max atteint"
        case _:
            return "autre"


assert check(100) == "max atteint"
assert check(50) == "autre"
assert check(200) == "autre"


print("Toutes les solutions passent ✅")
