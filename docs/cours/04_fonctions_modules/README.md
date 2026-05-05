# Chapitre 4 — Fonctions & scope

Les fonctions en Python sont des **objets de première classe** : on peut les passer en argument, les retourner, les stocker. Ce chapitre couvre en profondeur les paramètres (positionnels, nommés, `*args`, `**kwargs`, séparateurs `/` et `*`), la portée (LEGB), les closures, les type hints, et l'organisation en modules.

## 1. Définir une fonction

```python
def saluer(nom: str) -> str:
    """Retourne un message de salutation."""
    return f"Bonjour {nom} !"
```

- `nom: str` : **annotation** de type du paramètre
- `-> str` : annotation du type de retour
- Le triple-quote au début est la **docstring** (accessible via `saluer.__doc__`)

Les annotations ne sont **pas** vérifiées à l'exécution. Elles servent l'IDE et les type checkers comme `mypy`.

## 2. Les six catégories de paramètres

Python distingue **positionnel**, **positionnel ou nommé**, **nommé obligatoire**, **variadiques positionnel et nommé**. Les séparateurs `/` et `*` permettent de contrôler chaque zone.

Syntaxe complète :

```python
def f(pos_only, /, standard, *args, kw_only, **kwargs):
    ...
```

| Zone | Appel |
|---|---|
| Avant `/` | positionnel **uniquement** |
| Entre `/` et `*` (ou `*args`) | positionnel **ou** nommé |
| Après `*` ou `*args` | nommé **uniquement** |
| `*args` | tuple des positionnels restants |
| `**kwargs` | dict des nommés restants |

### Exemple détaillé

```python
def creer_user(id, /, nom, age=18, *, email, **extras):
    return {"id": id, "nom": nom, "age": age, "email": email, **extras}

# id : positional-only (pas d'appel `id=...`)
# nom, age : standard
# email : keyword-only (doit être nommé)
# extras : dict supplémentaire

creer_user(1, "Alice", email="a@a.com")                   # ✅
creer_user(1, nom="Alice", email="a@a.com")               # ✅
creer_user(id=1, nom="Alice", email="a@a.com")            # ❌ id est positional-only
creer_user(1, "Alice", 30, "a@a.com")                     # ❌ email doit être nommé
creer_user(1, "Alice", email="a@a.com", role="admin")     # ✅ role va dans extras
```

### Quand utiliser `*` (keyword-only)

Force l'appelant à nommer les arguments. Améliore la lisibilité quand il y a beaucoup de paramètres ou que les booléens rendent l'appel cryptique.

```python
def export(data, *, format="json", compress=False):
    ...

export(mes_donnees, format="csv", compress=True)   # ✅ explicite
export(mes_donnees, "csv", True)                    # ❌ refusé
```

### Quand utiliser `/` (positional-only)

Utile pour les fonctions où le nom du paramètre est un détail d'implémentation qu'on ne veut pas figer dans l'API (et qu'on veut pouvoir renommer librement).

```python
def len(obj, /):        # signature réelle de len, pour info
    ...
```

## 3. `*args` et `**kwargs`

```python
def somme(*args):
    return sum(args)

somme(1, 2, 3)            # 6
somme(1, 2, 3, 4, 5)      # 15
```

`args` est un **tuple**.

```python
def afficher(**kwargs):
    for cle, val in kwargs.items():
        print(f"{cle} = {val}")

afficher(nom="Alice", age=30)
```

`kwargs` est un **dict**.

### Unpacking à l'appel

```python
nombres = [1, 2, 3]
somme(*nombres)           # équivaut à somme(1, 2, 3)

params = {"nom": "Alice", "age": 30}
afficher(**params)        # équivaut à afficher(nom="Alice", age=30)
```

Pratique pour passer une config ou relayer des arguments (wrappers, décorateurs).

## 4. Portée (LEGB)

Python résout les noms dans cet ordre :

| | Nom | Description |
|---|---|---|
| **L** | Local | variables définies dans la fonction |
| **E** | Enclosing | scope des fonctions englobantes |
| **G** | Global | module (top-level) |
| **B** | Built-in | `print`, `len`, etc. |

```python
x = "global"

def externe():
    x = "enclosing"
    def interne():
        x = "local"
        print(x)          # "local"
    interne()
    print(x)              # "enclosing"

externe()
print(x)                  # "global"
```

### `global` et `nonlocal`

Par défaut, affecter une variable crée une variable **locale**. Pour modifier une variable existante à un scope supérieur :

```python
compteur = 0

def incremente():
    global compteur       # pour modifier la variable du module
    compteur += 1

def outer():
    x = 0
    def inner():
        nonlocal x        # pour modifier la variable de outer
        x += 1
    inner()
    return x
```

**Règle pratique** : évitez `global`. Préférez passer/retourner explicitement.

## 5. Closures

Une **closure** est une fonction qui capture des variables de son scope englobant.

```python
def multiplieur(facteur: int):
    def multiplier(x: int) -> int:
        return x * facteur       # facteur est capturé
    return multiplier

double = multiplieur(2)
triple = multiplieur(3)

double(10)    # 20
triple(10)    # 30
```

`double` et `triple` sont deux fonctions **différentes** qui se souviennent chacune de leur `facteur`. Accessible via `double.__closure__`.

### Piège classique : capture tardive dans une boucle

```python
fonctions = [lambda: i for i in range(3)]
[f() for f in fonctions]   # [2, 2, 2] et NON [0, 1, 2]
```

Toutes les lambdas capturent **la même** variable `i`, qui vaut `2` à la fin. Correction avec un argument par défaut :

```python
fonctions = [lambda i=i: i for i in range(3)]
[f() for f in fonctions]   # [0, 1, 2]
```

## 6. Fonctions comme objets de première classe

Une fonction peut être :

```python
# Assignée
f = saluer
f("Alice")

# Passée en argument
def applique(fonc, valeur):
    return fonc(valeur)

applique(str.upper, "hello")     # 'HELLO'

# Retournée
def choisir_op(op: str):
    operations = {"add": lambda a, b: a + b, "mul": lambda a, b: a * b}
    return operations[op]

plus = choisir_op("add")
plus(3, 4)                       # 7
```

### `lambda` : fonction anonyme

```python
carre = lambda x: x ** 2
carre(5)          # 25
```

Limites : **une seule expression**, pas de statements (`if`, `for`, etc.). À réserver aux cas très courts (tri, `map`, `filter`). Pour tout le reste, `def`.

```python
# Usage typique
personnes.sort(key=lambda p: p.age)
```

## 7. Type hints : bases

```python
def saluer(nom: str, age: int = 18) -> str:
    return f"{nom} a {age} ans"
```

### Collections génériques (3.9+)

```python
def moyenne(nombres: list[float]) -> float:
    return sum(nombres) / len(nombres)

def compter(mots: list[str]) -> dict[str, int]:
    ...
```

### Unions et optionnels (3.10+)

```python
def find(id: int) -> User | None:
    ...

def log(msg: str | bytes) -> None:
    ...
```

### Callable

```python
from collections.abc import Callable

def applique(fonc: Callable[[int], int], x: int) -> int:
    return fonc(x)
```

`Callable[[int], int]` = fonction prenant un `int` et retournant un `int`.

### `Any` et le cas où on ne sait pas

```python
from typing import Any

def log(msg: Any) -> None:
    print(msg)
```

`Any` = "désactive le type checker ici". À utiliser en dernier recours.

Le typage avancé (`Generic`, `TypeVar`, `Protocol`, etc.) est couvert au Ch. 10.

## 8. Docstrings

Une fonction publique doit avoir une docstring. Le style **Google** ou **NumPy** est standard ; choisissez-en un et tenez-vous-y.

```python
def diviser(a: float, b: float) -> float:
    """Divise a par b.

    Args:
        a: le dividende.
        b: le diviseur (non nul).

    Returns:
        Le résultat de a / b.

    Raises:
        ValueError: si b vaut 0.
    """
    if b == 0:
        raise ValueError("division par zéro")
    return a / b
```

Accessible via `help(diviser)` ou `diviser.__doc__`.

## 9. Modules et imports

Un **module** = un fichier `.py`. Un **paquet** = un dossier contenant `__init__.py` (ou implicitement depuis 3.3).

### Formes d'import

```python
import math                       # accès : math.sqrt
import math as m                  # alias
from math import sqrt             # accès direct : sqrt
from math import sqrt, pi         # plusieurs
from math import *                # ❌ à éviter (pollue le namespace)
```

### Imports absolus vs relatifs

Dans un paquet `mon_projet/`:

```python
# Import absolu (recommandé)
from mon_projet.utils import helper

# Import relatif (autorisé dans un paquet)
from .utils import helper
from ..other_package import thing
```

PEP 8 recommande les **absolus**. Les relatifs sont tolérés pour réorganisations faciles.

### `if __name__ == "__main__":`

Quand vous exécutez `python script.py`, la variable `__name__` du script vaut `"__main__"`. Quand vous l'importez, elle vaut `"script"`.

```python
# calcul.py
def carre(x):
    return x * x

if __name__ == "__main__":
    # Code exécuté uniquement lors de `python calcul.py`
    print(carre(5))
```

Permet d'avoir un module **importable** et **exécutable**.

## 10. Bibliothèque standard : le strict minimum à connaître

Python est "batteries included". Quelques modules essentiels :

| Module | Usage |
|---|---|
| `math` | `sqrt`, `pi`, `log`, `sin` |
| `random` | `randint`, `choice`, `shuffle` |
| `datetime` | `datetime.now()`, `timedelta` |
| `pathlib` | chemins de fichiers (Ch. 6) |
| `json` | `json.loads`, `json.dumps` |
| `re` | regex (Annexe B) |
| `collections` | `Counter`, `defaultdict` (Ch. 5) |
| `itertools`, `functools` | outils fonctionnels (Ch. 9) |
| `logging` | journalisation (Ch. 6) |

Règle : **avant d'installer un paquet tiers, vérifiez si la stdlib le couvre**.

---

### Piège courant : muter un argument par défaut

(Rappel du Ch. 2, mais dans le contexte fonction.)

```python
def ajoute(item, dest=[]):    # ❌ la liste est partagée entre appels
    dest.append(item)
    return dest
```

Fix :

```python
def ajoute(item, dest=None):
    if dest is None:
        dest = []
    dest.append(item)
    return dest
```

---

### Sous le capot : une fonction est un objet

```python
def f(x):
    """docstring"""
    return x * 2

f.__name__           # 'f'
f.__doc__            # 'docstring'
f.__defaults__       # None ou tuple des valeurs par défaut
f.__code__           # objet code compilé
f.__globals__        # le dict global du module où f est définie
f.custom_attr = 42   # oui, on peut ajouter des attributs sur une fonction
```

Ce n'est pas juste du sucre syntaxique. Les décorateurs (Ch. 11) exploitent cette nature d'objet.

---

## À retenir

- Signature complète : `def f(pos_only, /, standard, *args, kw_only, **kwargs)`.
- `*` force les arguments suivants à être nommés (lisibilité).
- LEGB : Local → Enclosing → Global → Builtin.
- Évitez `global`. Préférez retours explicites.
- Closures : fonctions qui capturent leur scope englobant.
- Fonctions = objets ; passables, retournables, stockables.
- Type hints : indicatifs, pas exécutoires. Activez `mypy`.
- `if __name__ == "__main__":` pour les modules importables + exécutables.

---

➡️ [Chapitre 5 — Structures de données](../05_structures_donnees/README.md)
