# Chapitre 9 — Itérateurs, générateurs, fonctionnel

Comprendre **comment** `for` fonctionne réellement, écrire des générateurs qui manipulent des flux de données sans saturer la RAM, exploiter `itertools` et `functools`. Sujet dense, mais indispensable pour tout code Python qui manipule des collections.

## 1. Le protocole d'itération

Quand vous écrivez `for x in obj:`, Python fait :

1. Appelle `iter(obj)` → récupère un **itérateur**.
2. Sur l'itérateur, appelle `next()` en boucle.
3. À chaque `next()`, reçoit une valeur ou l'exception `StopIteration` (fin).

### `__iter__` et `__next__`

Un **itérable** : a `__iter__` qui retourne un itérateur.
Un **itérateur** : a `__next__` (et `__iter__` qui retourne `self`).

```python
class CompteARebours:
    def __init__(self, n):
        self.n = n

    def __iter__(self):           # rend l'objet itérable
        return self

    def __next__(self):           # itère
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1


for x in CompteARebours(3):
    print(x)       # 3, 2, 1
```

**Note importante** : un itérateur s'épuise. Une fois parcouru, il ne peut pas redémarrer. D'où la distinction itérable (réutilisable) vs itérateur (usage unique).

```python
c = CompteARebours(3)
list(c)       # [3, 2, 1]
list(c)       # []  ← épuisé
```

### `iter()` avec sentinel — astuce

```python
# Lit un fichier par blocs jusqu'à rencontrer un bloc vide
with open("f.bin", "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        traiter(chunk)
```

`iter(callable, sentinel)` appelle la fonction jusqu'à ce qu'elle retourne la sentinelle.

## 2. Les générateurs (`yield`)

Écrire un itérateur avec `__iter__`/`__next__` est verbeux. Les générateurs simplifient ça.

```python
def compte_a_rebours(n):
    while n > 0:
        yield n
        n -= 1


for x in compte_a_rebours(3):
    print(x)       # 3, 2, 1
```

### Fonctionnement

Une fonction qui contient `yield` est un **générateur**. L'appeler ne l'exécute pas : ça retourne un **objet générateur**.

```python
g = compte_a_rebours(3)       # aucune ligne n'est exécutée
next(g)                        # 3 ; s'arrête au yield
next(g)                        # 2
next(g)                        # 1
next(g)                        # StopIteration
```

Entre deux `yield`, l'état de la fonction (variables locales, position du curseur) est **gelé**. Très économique : aucune liste n'est créée en mémoire.

### Pourquoi c'est puissant

```python
def lire_grosses_lignes(path):
    with open(path, encoding="utf-8") as f:
        for ligne in f:
            if len(ligne) > 100:
                yield ligne


# Traite un fichier de 10 Go sans en charger une seule ligne inutile
for l in lire_grosses_lignes("huge.log"):
    traiter(l)
```

Aucun stockage intermédiaire. L'opération est **pipelinée**.

### Expressions génératrices

```python
carres = (x ** 2 for x in range(1_000_000))     # parenthèses, pas crochets
total = sum(carres)     # calcul sans liste intermédiaire
```

À préférer systématiquement aux list comprehensions quand on ne garde pas le résultat.

### `yield from` — délégation

```python
def sous_gen():
    yield 1
    yield 2

def gen():
    yield 0
    yield from sous_gen()     # équivalent à `for x in sous_gen(): yield x`
    yield 3


list(gen())       # [0, 1, 2, 3]
```

### `send`, `throw`, `close` — générateurs avancés

Un générateur peut **recevoir** des valeurs :

```python
def accumulateur():
    total = 0
    while True:
        valeur = yield total     # yield RETOURNE ce qu'on lui envoie via send
        total += valeur


acc = accumulateur()
next(acc)           # amorce : avance jusqu'au premier yield, reçoit 0
acc.send(5)         # envoie 5, reçoit 5
acc.send(10)        # envoie 10, reçoit 15
acc.close()         # termine le générateur (GeneratorExit)
```

Rare en pratique : remplacé par `async/await` pour la plupart des cas (Ch. 12). Bon à connaître.

## 3. `itertools` — la boîte à outils

Le module `itertools` fournit des briques composables très efficaces.

### Infinis

```python
from itertools import count, cycle, repeat

count(10)           # 10, 11, 12, ...           (infini)
count(0, 2)         # 0, 2, 4, ...
cycle([1, 2, 3])    # 1, 2, 3, 1, 2, 3, ...     (infini)
repeat("a", 3)      # "a", "a", "a"
```

### Chainage et découpe

```python
from itertools import chain, islice

chain([1, 2], [3, 4], [5])        # 1, 2, 3, 4, 5
chain.from_iterable([[1, 2], [3]])# idem pour un iterable d'iterables

islice(range(100), 5)             # 0..4 (comme [0:5] mais lazy)
islice(range(100), 10, 20)        # 10..19
islice(range(100), 0, 100, 2)     # pas de 2
```

`islice` est le **slicing sans matérialiser** : utile sur des générateurs infinis.

### Groupement

```python
from itertools import groupby

data = [("a", 1), ("a", 2), ("b", 3), ("a", 4)]
for cle, groupe in groupby(data, key=lambda x: x[0]):
    print(cle, list(groupe))
# a [('a', 1), ('a', 2)]
# b [('b', 3)]
# a [('a', 4)]
```

**Piège** : `groupby` ne regroupe que les éléments **consécutifs** identiques. Pour grouper "tous les a ensemble", il faut **trier d'abord** par la même clé, ou utiliser `defaultdict`.

### Produit et combinaisons

```python
from itertools import product, permutations, combinations

list(product([1, 2], ["a", "b"]))    # [(1,'a'), (1,'b'), (2,'a'), (2,'b')]
list(permutations([1, 2, 3], 2))     # (1,2), (1,3), (2,1), (2,3), (3,1), (3,2)
list(combinations([1, 2, 3], 2))     # (1,2), (1,3), (2,3)
```

### `tee` : cloner un itérateur

```python
from itertools import tee

gen = (x for x in range(10))
a, b = tee(gen, 2)         # deux itérateurs indépendants
```

**Attention** : `tee` stocke les éléments en interne pour les rejouer. Sur un flux énorme, ça reconstruit la liste — usage malin nécessaire.

### `accumulate`, `pairwise`, `batched` (3.12+)

```python
from itertools import accumulate, pairwise, batched

list(accumulate([1, 2, 3, 4]))           # [1, 3, 6, 10] (sommes cumulatives)
list(accumulate([1, 2, 3], initial=100))  # [100, 101, 103, 106]

list(pairwise([1, 2, 3, 4]))              # [(1,2), (2,3), (3,4)]

list(batched(range(10), 3))                # [(0,1,2), (3,4,5), (6,7,8), (9,)]
```

`batched` (3.12+) : diviser en lots de taille fixe, très demandé.

## 4. `functools` — outils fonctionnels

### `@cache` et `@lru_cache`

Mémoïsation automatique d'une fonction pure.

```python
from functools import cache, lru_cache


@cache                 # cache illimité (3.9+)
def fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)


@lru_cache(maxsize=128)    # cache LRU de taille bornée
def charge_config(path):
    ...


fib(100)          # calculé en microsecondes grâce au cache
fib.cache_info()  # statistiques : hits, misses, taille
```

- `@cache` : cache illimité — peut saturer la RAM sur fonctions appelées avec beaucoup d'arguments différents.
- `@lru_cache(maxsize=N)` : remplace les entrées les moins récentes.

**Contrainte** : les arguments doivent être **hashables** (pas de list ni dict).

### `partial` — fixation d'arguments

```python
from functools import partial


def envoyer(dest, message, priorite):
    ...

# Crée une version "pré-configurée"
envoyer_urgent = partial(envoyer, priorite="haute")
envoyer_urgent("a@b", "alerte !")   # équivalent à envoyer("a@b", "alerte !", priorite="haute")
```

Très utilisé pour passer des callbacks à des APIs (threading, GUIs).

### `reduce`

```python
from functools import reduce

reduce(lambda a, b: a + b, [1, 2, 3, 4])      # 10 (identique à sum)
reduce(lambda a, b: a * b, [1, 2, 3, 4])      # 24
reduce(lambda a, b: a * b, [1, 2, 3, 4], 10)  # 240 (avec initial)
```

En pratique, préférez `sum`, `math.prod`, `min`, `max`, `functools.reduce` seulement pour des réductions non standard.

### `singledispatch` — surcharge par type

```python
from functools import singledispatch


@singledispatch
def serialise(obj):
    raise TypeError(f"unsupported: {type(obj).__name__}")


@serialise.register
def _(obj: int):
    return {"type": "int", "value": obj}


@serialise.register
def _(obj: str):
    return {"type": "str", "value": obj}


@serialise.register(list)
def _(obj):
    return [serialise(x) for x in obj]


serialise(42)          # {'type': 'int', 'value': 42}
serialise([1, "a"])    # [{'type': 'int', 'value': 1}, {'type': 'str', 'value': 'a'}]
```

Alternative pythonique au pattern visitor / méthodes polymorphes.

## 5. `map`, `filter`, `reduce` vs compréhensions

```python
# map + filter
list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, range(10))))

# Compréhension — PLUS LISIBLE
[x ** 2 for x in range(10) if x % 2 == 0]
```

**En Python, les compréhensions sont idiomatiques**. `map`/`filter` restent utiles quand :

- La fonction existe déjà (ex. `map(str, nombres)` est plus court que `[str(n) for n in nombres]`).
- On veut la laziness d'un itérateur (générateur expression fait aussi très bien l'affaire).

## 6. Les générateurs pour ETL / pipelines

Pattern typique : lire → transformer → filtrer → agréger, tout en lazy.

```python
def lire_csv(path):
    with open(path, encoding="utf-8") as f:
        for ligne in f:
            yield ligne.strip().split(",")


def parser_en_dict(lignes, entetes):
    for ligne in lignes:
        yield dict(zip(entetes, ligne))


def filtrer_actifs(records):
    for r in records:
        if r.get("actif") == "1":
            yield r


# Composition — rien n'est chargé en mémoire
pipeline = filtrer_actifs(parser_en_dict(
    lire_csv("users.csv"),
    ["id", "nom", "actif"],
))

total_actifs = sum(1 for _ in pipeline)
```

C'est la manière Python-native d'écrire du traitement de flux. Performant, composable, testable.

---

### Piège courant : épuiser un générateur en le "vérifiant"

```python
g = (x for x in range(10))
if g:         # ❌ un générateur est TOUJOURS truthy, tant qu'il existe !
    print(list(g))
```

Un générateur est toujours truthy (c'est un objet). Vérifier s'il est vide exige de le consommer. Pour y voir clair : matérialiser en `list` si besoin, ou gérer l'absence d'éléments dans la consommation (`for x in g: ...; else: ...`).

---

### Sous le capot : pourquoi les générateurs sont efficaces

Un générateur n'exécute pas sa fonction entière : il **suspend** son état entre deux `yield`. En CPython, cela utilise une **frame** persistante (au lieu de la détruire à chaque appel comme une fonction normale). Chaque `next()` restaure la frame, exécute jusqu'au prochain `yield`, puis la gèle à nouveau.

C'est ce qui permet d'avoir des "coroutines" — et c'est aussi la fondation historique d'`asyncio` (Ch. 12).

---

## À retenir

- Itérable = `__iter__`. Itérateur = `__iter__` + `__next__`. Un itérateur s'épuise.
- Générateurs (`yield`) = itérateurs faciles à écrire.
- Expression génératrice `(x for x in ...)` au lieu de liste quand on ne garde pas.
- `itertools` : `chain`, `islice`, `groupby`, `product`, `pairwise`, `batched`.
- `functools` : `cache`/`lru_cache`, `partial`, `singledispatch`.
- Compréhensions > `map`/`filter` dans la plupart des cas.
- Pipelines de générateurs = paradigme naturel pour le traitement de flux.

---

➡️ [Chapitre 10 — Typage statique & qualité](../10_tests_qualite/README.md)
