# Chapitre 3 — Flux de contrôle

Conditions, boucles, et **pattern matching structurel**. Ce chapitre va plus loin que le sempiternel `if/else` : chaînages de comparaison, truthiness, clause `else` sur les boucles, walrus, et pattern matching en profondeur.

## 1. Conditions

### Syntaxe

```python
if score >= 90:
    mention = "excellent"
elif score >= 70:
    mention = "bien"
elif score >= 50:
    mention = "passable"
else:
    mention = "insuffisant"
```

L'**indentation** (4 espaces par convention, PEP 8) délimite les blocs. Pas d'accolades.

### Opérateur ternaire

```python
statut = "majeur" if age >= 18 else "mineur"
```

À utiliser pour une affectation simple. Au-delà, préférez un vrai `if`.

### Chaînage de comparaisons (trop peu utilisé)

Python permet d'écrire :

```python
if 0 <= age < 120:           # équivalent à : 0 <= age and age < 120
    ...

if a == b == c:              # les trois doivent être égaux
    ...
```

Plus lisible que `if 0 <= age and age < 120`. Et plus efficace : chaque variable est évaluée une seule fois.

### Truthiness (rappel du Ch. 2)

```python
if ma_liste:                 # ✅ pythonique
    traiter(ma_liste)

if len(ma_liste) > 0:        # ❌ verbeux
    traiter(ma_liste)

if user is not None:         # ✅ explicite pour None
    ...
```

Règle : testez l'objet directement pour les collections, utilisez `is None` pour distinguer "absent" de "vide".

## 2. Opérateurs logiques et court-circuit

```python
a and b      # b si a est truthy, sinon a
a or b       # a si a est truthy, sinon b
not a        # True si a est falsy
```

**Attention** : `and` et `or` ne retournent pas toujours un booléen.

```python
"" or "défaut"           # 'défaut'
"salut" or "défaut"      # 'salut'
[] and "x"               # []
"a" and "b"              # 'b'
```

Usage idiomatique :

```python
nom = nom_user or "anonyme"   # défaut si falsy
```

**Court-circuit** : `and` et `or` évaluent leur deuxième opérande seulement si nécessaire.

```python
if user is not None and user.est_admin:    # ✅ sûr
    ...
# Si user est None, user.est_admin n'est pas évalué (pas d'AttributeError)
```

## 3. La boucle `for`

En Python, `for` itère sur un **itérable** (tout objet ayant `__iter__`). Il n'existe pas de `for (i=0; i<n; i++)` style C.

```python
for lettre in "python":
    print(lettre)

for nom in ["Alice", "Bob"]:
    print(nom)

for cle, valeur in {"a": 1, "b": 2}.items():
    print(cle, valeur)
```

### `range(start, stop, step)`

```python
range(5)           # 0, 1, 2, 3, 4
range(1, 6)        # 1, 2, 3, 4, 5
range(0, 10, 2)    # 0, 2, 4, 6, 8
range(10, 0, -1)   # 10, 9, 8, ..., 1
```

`range` est **paresseux** (lazy) : il ne stocke pas tous les entiers, il les produit à la demande.

### `enumerate()` et `zip()`

Pour avoir l'index :

```python
for i, nom in enumerate(["Alice", "Bob"], start=1):
    print(f"{i}. {nom}")    # 1. Alice / 2. Bob
```

Pour itérer en parallèle :

```python
noms = ["Alice", "Bob"]
ages = [30, 25]
for nom, age in zip(noms, ages):
    print(f"{nom} : {age}")
```

**Piège de `zip`** : s'arrête au plus court. Pour forcer la même longueur (ou échouer si ce n'est pas le cas) :

```python
for x, y in zip(l1, l2, strict=True):   # 3.10+ : lève ValueError si longueurs différentes
    ...
```

### La clause `else` sur les boucles (méconnue)

Une boucle `for` ou `while` peut avoir un `else`. Il s'exécute si la boucle se termine **sans `break`**.

```python
for nombre in nombres:
    if nombre < 0:
        print("Valeur négative trouvée !")
        break
else:
    print("Tous les nombres sont positifs.")
```

Cas d'usage typique : recherche avec signalement d'échec.

## 4. La boucle `while`

```python
compteur = 5
while compteur > 0:
    print(compteur)
    compteur -= 1
```

À réserver aux cas où le nombre d'itérations n'est pas connu à l'avance (attente d'une condition, boucle événementielle). Dès qu'on itère sur une séquence connue, préférez `for`.

### `break` et `continue`

```python
for n in range(100):
    if n == 10:
        break            # sort de la boucle
    if n % 2 == 0:
        continue         # passe à l'itération suivante
    print(n)             # imprime 1, 3, 5, 7, 9
```

## 5. L'opérateur walrus `:=` (3.8+)

Affecte **et** retourne une valeur. Évite de répéter un appel coûteux.

```python
# Avant walrus
data = fetch_data()
while data:
    traiter(data)
    data = fetch_data()

# Avec walrus
while (data := fetch_data()):
    traiter(data)
```

Autre cas d'usage : lire un fichier ligne par ligne.

```python
with open("log.txt") as f:
    while (line := f.readline()):
        traiter(line)
```

Dans les compréhensions, il évite de recalculer :

```python
# Filtrer + transformer avec calcul intermédiaire
resultats = [y for x in data if (y := transforme(x)) is not None]
```

**N'en abusez pas** : walrus mal placé rend le code cryptique.

## 6. Pattern matching structurel (3.10+)

Le `match/case` n'est **pas** un simple `switch`. C'est de la **correspondance de motifs** : il teste la structure et lie des variables.

### Cas d'usage : valeurs littérales

```python
match commande:
    case "start":
        demarrer()
    case "stop":
        arreter()
    case "restart":
        redemarrer()
    case _:                 # wildcard, toujours en dernier
        raise ValueError(f"Commande inconnue : {commande}")
```

Déjà plus lisible qu'une cascade `if/elif`.

### Cas d'usage : OR pattern

```python
match commande:
    case "quit" | "exit" | "q":
        sortir()
    case _:
        ...
```

### Cas d'usage : déstructuration de séquences

```python
def analyse(cmd: list[str]) -> str:
    match cmd:
        case []:
            return "commande vide"
        case [action]:
            return f"action simple : {action}"
        case [action, cible]:
            return f"{action} sur {cible}"
        case [action, *cibles]:
            return f"{action} sur {len(cibles)} cibles"
```

Le `*cibles` capture le reste. Puissant.

### Cas d'usage : déstructuration de dictionnaires

```python
match event:
    case {"type": "click", "x": x, "y": y}:
        print(f"clic en ({x}, {y})")
    case {"type": "key", "key": touche}:
        print(f"touche {touche}")
    case {"type": type_, **reste}:
        print(f"événement {type_} avec {reste}")
```

Contrairement à l'égalité stricte de dict, le match vérifie que les clés listées **sont présentes** — des clés supplémentaires sont ignorées (sauf si `**reste` est utilisé).

### Cas d'usage : types et attributs (class patterns)

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Cercle:
    centre: Point
    rayon: float

def decrire(forme):
    match forme:
        case Point(x=0, y=0):
            return "origine"
        case Point(x=x, y=y):
            return f"point en ({x}, {y})"
        case Cercle(centre=Point(x=0, y=0), rayon=r):
            return f"cercle centré à l'origine de rayon {r}"
        case Cercle(rayon=r) if r > 10:          # garde !
            return f"grand cercle (rayon {r})"
        case Cercle(centre=c, rayon=r):
            return f"cercle en {c} de rayon {r}"
```

Notez la **garde** `if r > 10` : condition supplémentaire.

### Piège : les noms de variables capturent

```python
TAILLE_MAX = 100

match x:
    case TAILLE_MAX:        # ❌ NE teste PAS l'égalité avec TAILLE_MAX
        ...                 # capture x dans une variable nommée TAILLE_MAX !
```

Un nom non qualifié dans un case est **une liaison**. Pour comparer à une constante, utilisez `.` :

```python
class Config:
    TAILLE_MAX = 100

match x:
    case Config.TAILLE_MAX:        # ✅ compare à Config.TAILLE_MAX
        ...
```

Ou wrappez dans un garde :

```python
match x:
    case n if n == TAILLE_MAX:
        ...
```

### Quand utiliser `match` vs `if`

- `if/elif` : conditions hétérogènes, logique métier complexe, 2-3 branches.
- `match` : vous testez la **structure** (type, forme) d'une donnée. Typique : AST, parseurs, états d'un automate, payloads JSON variés.

---

### Piège courant : oublier le `_` final

```python
match commande:
    case "start": ...
    case "stop": ...
```

Si `commande` vaut `"restart"`, rien ne se passe, **silencieusement**. Toujours prévoir `case _:` — même pour lever une exception.

---

### Sous le capot : pourquoi `match` n'est pas juste un switch

Le compilateur Python transforme `match` en un bytecode optimisé utilisant `MATCH_SEQUENCE`, `MATCH_MAPPING`, `MATCH_CLASS`. Les patterns de séquence sont compilés en vérifications de longueur + accès indexés. Les patterns de classe vérifient `isinstance` + extraient les attributs déclarés via `__match_args__` (présent par défaut sur les dataclasses).

---

## À retenir

- Chaînage de comparaisons : `if 0 <= x < 10`.
- `and`/`or` retournent une des opérandes, pas forcément un booléen.
- `for/else` et `while/else` : exécuté si pas de `break`.
- `enumerate`, `zip(..., strict=True)` : idiomatiques.
- Walrus `:=` : affecter dans une expression, sans abuser.
- `match/case` = correspondance de motifs, pas un switch. Déstructure les données.
- Attention aux noms non qualifiés dans `case` : ils **capturent**.

---

➡️ [Chapitre 4 — Fonctions & scope](../04_fonctions_modules/README.md)
