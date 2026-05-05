# Chapitre 5 — Structures de données

Les quatre collections built-in (`list`, `tuple`, `dict`, `set`), leurs variantes du module `collections`, les compréhensions, et — point souvent oublié — la **complexité algorithmique** de chaque opération. Choisir la bonne structure divise par 100 le temps d'un programme sans changer son comportement.

## 1. Les quatre collections principales

| Structure | Mutable | Ordonnée | Duplicats | Indexée | Syntaxe |
|---|---|---|---|---|---|
| `list` | ✅ | ✅ | ✅ | par position | `[1, 2, 3]` |
| `tuple` | ❌ | ✅ | ✅ | par position | `(1, 2, 3)` |
| `dict` | ✅ | ✅ (insertion) | clés uniques | par clé | `{"a": 1}` |
| `set` | ✅ | ❌ | ❌ (uniques) | ❌ | `{1, 2, 3}` |

**Depuis Python 3.7** : les `dict` préservent l'ordre d'insertion (garanti par la spec). Ne comptez plus `OrderedDict` comme nécessaire pour ça.

## 2. `list` — liste dynamique

```python
notes = [15, 12, 18, 10]
notes.append(14)            # fin
notes.insert(0, 20)         # début (O(n) !)
notes.extend([8, 9])        # ajout de plusieurs
notes.remove(10)            # par valeur
del notes[0]                # par index
notes.pop()                 # retire et retourne le dernier
```

### Slicing

Identique aux strings, mais une liste est mutable :

```python
nums = [0, 1, 2, 3, 4, 5]
nums[1:4]              # [1, 2, 3]
nums[::2]              # [0, 2, 4]
nums[::-1]             # [5, 4, 3, 2, 1, 0]
nums[1:4] = [99, 99]   # remplacement ! nums == [0, 99, 99, 4, 5]
```

### Tri

```python
nums.sort()                    # en place, modifie nums
nums.sort(reverse=True)
nums.sort(key=abs)             # par critère

sorted(nums)                   # retourne une NOUVELLE liste, nums intact
sorted(personnes, key=lambda p: p.age)
```

Clé composée :

```python
sorted(users, key=lambda u: (u.age, u.nom))   # tri par âge puis nom
```

### Performance de `list`

| Opération | Complexité | Note |
|---|---|---|
| `l[i]` accès | O(1) | |
| `l.append(x)` | O(1) amorti | réallocation occasionnelle |
| `l.pop()` | O(1) | fin |
| `l.insert(0, x)` | O(n) | décale tout |
| `l.pop(0)` | O(n) | idem |
| `x in l` | O(n) | parcours linéaire |
| `l[i:j]` | O(j-i) | copie |
| `len(l)` | O(1) | stocké |

**Conséquence** : si vous insérez/retirez souvent au début, utilisez `collections.deque` (voir §7).

## 3. `tuple` — immuable et léger

```python
point = (3, 4)
x, y = point              # unpacking
```

### Pourquoi un tuple plutôt qu'une liste ?

- **Immuabilité** : garantit qu'il ne sera pas modifié par erreur (contrats).
- **Hashable** : utilisable comme clé de `dict` ou élément de `set`.
- **Performance** : légèrement plus rapide et plus économe en mémoire.

```python
positions = {(0, 0): "départ", (5, 3): "arrivée"}   # clés tuple OK
positions = {[0, 0]: "départ"}                       # ❌ TypeError: unhashable
```

### Named tuples et dataclasses

Pour un tuple nommé, deux options :

```python
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x, p.y

# Mieux (3.6+) : dataclass frozen (Ch. 7)
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float
```

## 4. `dict` — table de hachage

```python
user = {"nom": "Alice", "age": 30}
user["email"] = "a@a.com"     # ajout/modif
del user["age"]
"nom" in user                  # True (test de présence)
user.get("age", 0)             # 0 si absent (pas d'exception)
```

### Parcours

```python
for cle in user:              # itère les clés
    ...
for cle, val in user.items():  # couples (préféré)
    ...
for val in user.values():
    ...
```

### Méthodes utiles

```python
user.setdefault("role", "user")   # ajoute si absent, retourne la valeur
user.pop("email", None)            # retire et retourne, défaut si absent
user.update({"age": 31})           # fusionne

# Fusion d'opérateurs (3.9+)
nouveau = dict1 | dict2           # union (dict2 gagne sur les clés communes)
dict1 |= dict2                     # fusion en place
```

### Performance de `dict`

| Opération | Complexité |
|---|---|
| `d[k]` accès | O(1) amorti |
| `d[k] = v` | O(1) amorti |
| `k in d` | O(1) amorti |
| `del d[k]` | O(1) amorti |
| `len(d)` | O(1) |

Les "amorti" cachent les collisions de hash (rares) et les réallocations.

### Contraintes sur les clés

Les clés doivent être **hashables** (`__hash__` défini). En pratique :
- OK : `int`, `float`, `str`, `tuple` de hashables, `frozenset`, dataclass `frozen=True`
- Non : `list`, `dict`, `set`, instance de classe mutable par défaut

## 5. `set` — ensemble de valeurs uniques

```python
tags = {"python", "web", "async"}
tags.add("api")
tags.remove("web")              # KeyError si absent
tags.discard("web")             # silencieux
```

### Opérations ensemblistes

```python
a = {1, 2, 3}
b = {2, 3, 4}

a | b       # union           {1, 2, 3, 4}
a & b       # intersection    {2, 3}
a - b       # différence      {1}
a ^ b       # diff symétrique {1, 4}
a <= b      # sous-ensemble ?
```

### Cas d'usage typiques

```python
# Dédoublonner
mots_uniques = set(mots)

# Test d'appartenance rapide (O(1) vs O(n) pour une liste)
vus = set()
for item in items:
    if item not in vus:
        traiter(item)
        vus.add(item)
```

### `frozenset` : set immuable et hashable

```python
tags = frozenset({"python", "web"})
# tags.add(...) -> AttributeError
# MAIS : utilisable comme clé de dict
```

## 6. Compréhensions

Syntaxe condensée pour construire une collection.

### List comprehension

```python
# Classique :
carres = []
for x in range(10):
    carres.append(x ** 2)

# Compréhension :
carres = [x ** 2 for x in range(10)]

# Avec filtre :
pairs = [x for x in range(20) if x % 2 == 0]

# Imbriquée :
matrice = [[i * j for j in range(3)] for i in range(3)]
```

### Dict comprehension

```python
inverses = {v: k for k, v in user.items()}
carres = {x: x ** 2 for x in range(5)}
```

### Set comprehension

```python
extensions = {f.suffix for f in fichiers}
```

### Expression génératrice (lazy, **pas** une compréhension)

```python
# Parenthèses = lazy, aucune liste construite
total = sum(x ** 2 for x in range(1_000_000))
```

Plus économe en mémoire : aucun stockage intermédiaire. Couvert en profondeur au Ch. 9.

### Quand ne PAS utiliser une compréhension

- Plus de **2 niveaux** imbriqués → boucle classique, plus lisible.
- Logique complexe dans la condition ou l'expression → boucle classique.
- Effets de bord → **jamais** en compréhension.

```python
# ❌ effet de bord dans compréhension
[print(x) for x in items]

# ✅
for x in items:
    print(x)
```

## 7. `collections` — structures spécialisées

### `Counter` — compteur

```python
from collections import Counter

votes = ["a", "b", "a", "c", "a", "b"]
c = Counter(votes)
c                      # Counter({'a': 3, 'b': 2, 'c': 1})
c.most_common(2)       # [('a', 3), ('b', 2)]
c["d"]                 # 0 (pas de KeyError)
```

### `defaultdict` — dict avec défaut automatique

```python
from collections import defaultdict

groupes = defaultdict(list)
for user in users:
    groupes[user.role].append(user)   # pas besoin de vérifier si la clé existe
```

Sans `defaultdict` :

```python
groupes = {}
for user in users:
    groupes.setdefault(user.role, []).append(user)
```

### `deque` — file à double extrémité

```python
from collections import deque

q = deque([1, 2, 3])
q.appendleft(0)        # O(1) au début, contrairement à list.insert(0, ...)
q.popleft()            # O(1)
q.append(4)            # O(1)
q.pop()                # O(1)

# Utile aussi : buffer circulaire
recent = deque(maxlen=10)   # ne garde que les 10 derniers
```

### `namedtuple` — tuple nommé léger

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x, p.y              # accès nommé
p[0], p[1]            # accès indexé (c'est un tuple !)
```

Pour un besoin plus riche (méthodes, défauts, typing), préférez `dataclass` (Ch. 7).

## 8. Unpacking

```python
a, b = 1, 2                  # basique
a, b = b, a                  # swap, sans variable temporaire

a, *reste = [1, 2, 3, 4]     # a=1, reste=[2, 3, 4]
*debut, fin = [1, 2, 3, 4]   # debut=[1, 2, 3], fin=4
a, *milieu, z = [1, 2, 3, 4, 5]   # a=1, milieu=[2, 3, 4], z=5

# Dans les appels de fonction
def f(a, b, c): ...
args = (1, 2, 3)
f(*args)

# Fusion de dicts (3.5+)
fusion = {**dict1, **dict2}   # dict2 gagne sur les clés communes
```

---

### Piège courant : hash d'objet mutable

Tenter d'utiliser une liste comme clé :

```python
d = {[1, 2]: "oups"}    # TypeError: unhashable type: 'list'
```

Les listes changent, donc leur hash changerait, cassant l'invariant du dict. Si vous voulez une clé composite, utilisez un `tuple`.

---

### Piège courant : itérer et modifier en même temps

```python
for x in ma_liste:
    if condition(x):
        ma_liste.remove(x)     # ❌ comportement indéfini
```

Deux corrections :

```python
# A) Filtrer par compréhension
ma_liste = [x for x in ma_liste if not condition(x)]

# B) Itérer sur une copie
for x in ma_liste[:]:
    if condition(x):
        ma_liste.remove(x)
```

---

### Sous le capot : pourquoi `dict` est O(1)

Un `dict` est une **table de hachage**. Pour `d[k]` :

1. Calcule `hash(k)`.
2. Utilise le hash pour indexer un tableau interne.
3. Résout les collisions par open addressing.

La clé doit être **hashable** et son `__hash__` stable sur sa durée de vie. C'est pour ça que les objets mutables (listes) ne peuvent pas être des clés : leur hash changerait au fil des modifications.

---

## Choisir la bonne structure — récap

| Besoin | Structure |
|---|---|
| Séquence ordonnée, modifiable | `list` |
| Séquence ordonnée, figée, hashable | `tuple` |
| Association clé → valeur | `dict` |
| Set de valeurs uniques, test d'appartenance rapide | `set` |
| Insert/retire aux DEUX extrémités | `deque` |
| Comptage | `Counter` |
| Groupement par clé sans init | `defaultdict(list)` |
| Point nommé immuable | `dataclass(frozen=True, slots=True)` ou `namedtuple` |

## À retenir

- Connaître la complexité O() de chaque opération évite des bugs de performance.
- `list.insert(0, x)` et `list.pop(0)` sont O(n) → `deque`.
- Les clés de `dict` et éléments de `set` doivent être **hashables**.
- Compréhensions oui, effets de bord non.
- `collections` contient des structures spécialisées, apprenez-les.
- Unpacking étendu (`*reste`) est très expressif, utilisez-le.

---

➡️ [Chapitre 6 — I/O, exceptions, logging](../06_fichiers_exceptions/README.md)
