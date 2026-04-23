# Chapitre 2 — Modèle objet & types primitifs

Ce chapitre pose la fondation conceptuelle qui distingue les développeurs Python débutants des compétents : comprendre que **tout est objet**, et ce que cela implique pour l'identité, la mutabilité et les références.

## 1. Tout est objet

En Python, **tout** ce que vous manipulez est un objet : un entier, une fonction, une classe, un module. Chaque objet a **trois** caractéristiques :

| Caractéristique | Description | Fonction |
|---|---|---|
| **Identité** | Adresse mémoire, unique et fixe | `id(obj)` |
| **Type** | Nature de l'objet (détermine les opérations valides) | `type(obj)` |
| **Valeur** | Le contenu | affichage direct |

```python
x = 42
id(x)       # ex : 4391763728 (entier différent à chaque run)
type(x)     # <class 'int'>
x           # 42
```

Une **variable** en Python n'est pas une boîte contenant une valeur. C'est une **étiquette** collée sur un objet en mémoire. Plusieurs étiquettes peuvent pointer vers le même objet.

```python
a = [1, 2, 3]
b = a             # b pointe vers LE MÊME objet que a
b.append(4)
print(a)          # [1, 2, 3, 4] — surprise pour les débutants
print(id(a) == id(b))   # True
```

## 2. `is` vs `==` — identité vs égalité

- `a == b` : les **valeurs** sont-elles égales ? (appelle `__eq__`)
- `a is b` : les **identités** sont-elles les mêmes ? (même objet en mémoire)

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b      # True (même contenu)
a is b      # False (deux objets distincts)

c = a
a is c      # True (même étiquette)
```

> **Règle pratique** : utilisez `is` uniquement pour comparer à `None`, `True`, `False` (singletons). Pour tout le reste, `==`.

```python
if x is None:     # ✅ correct
    ...
if x is 0:        # ❌ incorrect, UB, warning depuis 3.8
    ...
```

### Le piège du small int cache

CPython met en cache les entiers de -5 à 256 pour la performance. Deux variables pointant vers `5` partagent l'objet. Au-delà, plus de garantie.

```python
a = 256; b = 256
a is b    # True (caché)

a = 257; b = 257
a is b    # False (deux objets 257 distincts) — MAIS dépend du contexte !
```

Ne vous appuyez **jamais** sur ce comportement. Utilisez `==`.

## 3. Mutabilité : la ligne de faille

Chaque type est soit **mutable** (modifiable en place), soit **immuable**.

| Immuables | Mutables |
|---|---|
| `int`, `float`, `bool`, `complex` | `list`, `dict`, `set`, `bytearray` |
| `str` | objets définis par vous (classes) — par défaut |
| `tuple` | |
| `frozenset`, `bytes` | |

### Conséquence n°1 : passage d'arguments

Python passe les arguments par **référence d'objet**. Modifier un objet mutable dans une fonction affecte l'appelant.

```python
def ajoute(liste):
    liste.append(99)   # modifie l'objet

ma_liste = [1, 2]
ajoute(ma_liste)
print(ma_liste)        # [1, 2, 99]
```

Avec un immuable, aucun risque : toute "modification" crée un nouvel objet.

```python
def incremente(n):
    n += 1             # crée un NOUVEL int, n pointe maintenant vers lui
                       # l'original est intact
a = 5
incremente(a)
print(a)               # 5
```

### Conséquence n°2 : le piège de l'argument par défaut mutable

```python
def ajoute_item(item, liste=[]):   # ❌ PIÈGE
    liste.append(item)
    return liste

ajoute_item(1)    # [1]
ajoute_item(2)    # [1, 2] ← ??
```

L'argument par défaut est évalué **une seule fois**, à la définition. La même liste est réutilisée à chaque appel. Correction :

```python
def ajoute_item(item, liste=None):
    if liste is None:
        liste = []
    liste.append(item)
    return liste
```

Retenez : **jamais de valeur par défaut mutable**. C'est une règle absolue.

## 4. Types numériques

### `int` : entiers de précision arbitraire

Contrairement à C ou Java, les entiers Python n'ont **pas de taille maximale**.

```python
10 ** 100   # calcule, aucun overflow
```

### `float` : IEEE 754 double précision

Les flottants ont les pièges habituels :

```python
0.1 + 0.2 == 0.3   # False !
0.1 + 0.2          # 0.30000000000000004
```

Pour de l'arithmétique exacte (finance, comptabilité), utilisez `decimal.Decimal` ou `fractions.Fraction`.

```python
from decimal import Decimal
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")   # True
```

### `bool` : sous-classe de `int`

```python
isinstance(True, int)   # True !
True + True             # 2
```

Utile parfois (compter des conditions vraies avec `sum(...)`), dangereux souvent.

### Opérateurs

```python
a, b = 10, 3
a + b     # 13
a - b     # 7
a * b     # 30
a / b     # 3.333... (division flottante)
a // b    # 3       (division entière, "floor division")
a % b     # 1       (modulo)
a ** b    # 1000    (puissance)
divmod(a, b)   # (3, 1) — quotient et reste
```

## 5. Chaînes de caractères (`str`)

Une `str` est une séquence immuable de caractères Unicode.

```python
s = "café"
len(s)         # 4 (caractères, pas octets)
s.encode()     # b'caf\xc3\xa9' (bytes UTF-8, 5 octets)
```

### Slicing

```python
s = "bonjour"
s[0]      # 'b'
s[-1]     # 'r'
s[0:3]    # 'bon'
s[::2]    # 'bnor' (un caractère sur deux)
s[::-1]   # 'ruojnob' (inversé)
```

### Méthodes essentielles

```python
s = "  Hello, World  "
s.strip()             # 'Hello, World'
s.lower()             # '  hello, world  '
s.replace("World", "Python")
s.split(",")          # ['  Hello', ' World  ']
",".join(["a", "b"])  # 'a,b'
"abc".startswith("a") # True
```

Toutes renvoient un **nouveau** string (immutabilité).

### f-strings (Python 3.6+, enrichies en 3.12)

La manière moderne de formater :

```python
nom = "Alice"
age = 30

f"{nom} a {age} ans"              # 'Alice a 30 ans'
f"{age + 1}"                      # '31' (expressions autorisées)
f"{age:03d}"                      # '030' (format spec)
f"{3.14159:.2f}"                  # '3.14'
f"{nom=}"                         # "nom='Alice'" (debug, 3.8+)
f"{nom!r}"                        # "'Alice'" (repr)
f"{'=' * 10}"                     # '==========' (expression arbitraire)
```

Le format spec suit la [mini-langue de `format()`](https://docs.python.org/3/library/string.html#format-specification-mini-language) :

```python
f"{1234567:,}"     # '1,234,567' (séparateur milliers)
f"{0.5:.1%}"       # '50.0%' (pourcentage)
f"{255:08b}"       # '11111111' (binaire padded)
f"{255:#x}"        # '0xff' (hexa avec préfixe)
```

## 6. `None`

`None` est l'objet qui représente "rien". Singleton : il n'y en a qu'un.

```python
x = None
x is None     # True ← toujours utiliser `is`
type(None)    # <class 'NoneType'>
```

Utilisé pour : valeur par défaut explicite, absence de retour d'une fonction, etc.

## 7. `type()` vs `isinstance()`

```python
type(x) == int            # vérifie le type EXACT
isinstance(x, int)        # True aussi pour les sous-classes
isinstance(True, int)     # True (bool hérite d'int)
```

**Utilisez `isinstance()`** sauf si vous avez une bonne raison. Il gère l'héritage correctement.

`isinstance()` accepte un tuple :

```python
isinstance(x, (int, float))   # True si x est l'un ou l'autre
```

## 8. Conversions de types

```python
int("42")      # 42
int("42", 16)  # 66 (parse en base 16)
float("3.14")  # 3.14
str(42)        # '42'
bool(0)        # False
bool("")       # False
bool([])       # False
bool(" ")      # True (string non vide)
```

### Truthiness

Ces valeurs sont **falsy** (évaluées à `False` dans un `if`) :

- `False`, `None`
- `0`, `0.0`, `0j`
- `""`, `[]`, `{}`, `()`, `set()`
- objets custom avec `__bool__` retournant `False` ou `__len__` retournant 0

Tout le reste est **truthy**.

```python
if ma_liste:         # ✅ pythonique
    traiter(ma_liste)

if len(ma_liste) > 0:   # ❌ verbeux, non idiomatique
    traiter(ma_liste)
```

## 9. Type hints — bases

Depuis Python 3.5 on peut annoter les types. Cela ne change **rien** à l'exécution, mais aide l'IDE et `mypy`.

```python
age: int = 25
nom: str = "Alice"
prix: float = 19.99
actif: bool = True
surnom: str | None = None       # 3.10+ (union)
```

Syntaxe moderne (3.9+) pour les génériques :

```python
scores: list[int] = [1, 2, 3]
config: dict[str, int] = {"port": 8000}
```

On approfondira au Ch. 4 et 10.

## 10. Interaction utilisateur : `input()` et `print()`

```python
nom = input("Votre nom ? ")    # toujours une str !
age = int(input("Votre âge ? "))    # conversion explicite
```

`print()` accepte plusieurs arguments et options :

```python
print("a", "b", sep="-")         # 'a-b'
print("ligne 1", end="")          # pas de retour à la ligne
print("erreur", file=sys.stderr)  # sortie d'erreur
```

---

### Piège courant : la copie superficielle

Copier un objet mutable n'est pas trivial :

```python
a = [[1, 2], [3, 4]]
b = a.copy()            # copie SUPERFICIELLE
b[0].append(99)
print(a)                # [[1, 2, 99], [3, 4]] ← aïe
```

`copy()` duplique la liste externe mais pas les sous-listes. Pour une copie **profonde** :

```python
import copy
b = copy.deepcopy(a)
```

---

### Sous le capot : pourquoi `==` peut être lent

Par défaut, `a == b` appelle `a.__eq__(b)`. Pour un gros objet, ça peut parcourir toute la structure. `is` est toujours O(1) (comparaison d'adresses). D'où la règle : `is None` > `== None`.

---

## À retenir

- Tout est objet ; chaque objet a identité, type, valeur.
- Une variable est une étiquette, pas une boîte.
- `is` pour identité (surtout `None`), `==` pour égalité.
- Mutabilité : source n°1 des bugs subtils. **Jamais de défaut mutable**.
- f-strings partout, format spec maîtrisé.
- `isinstance()` > `type() ==`.

---

➡️ [Chapitre 3 — Flux de contrôle](../03_flux_controle/README.md)
