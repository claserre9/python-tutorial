# Chapitre 14 — Performance & internals CPython

Quand Python est "trop lent", c'est **presque toujours** parce qu'on manque d'outils pour mesurer et qu'on fait des choix de structures inadaptés. Ce chapitre donne les outils (**profilage**), les techniques (**`__slots__`**, `weakref`, **gc**), et le bon état d'esprit pour optimiser.

## 1. Règle n°1 : **mesurer avant d'optimiser**

> "Premature optimization is the root of all evil." — Donald Knuth

Avant toute optimisation :
1. Le code est-il **correct** et **testé** ?
2. Est-il réellement **trop lent** pour le besoin ?
3. **Où** exactement est-il lent ? (profil, pas intuition)

## 2. `timeit` — micro-benchmark

Pour comparer rapidement deux implémentations.

```python
from timeit import timeit

timeit("sum([i*i for i in range(1000)])", number=10_000)
timeit("sum(i*i for i in range(1000))",   number=10_000)
```

En ligne de commande :

```bash
python -m timeit "sum([i*i for i in range(1000)])"
```

Ou dans IPython : `%timeit expr`.

**Piège** : `timeit` exécute plusieurs fois pour amortir le bruit, mais les micro-benchmarks peuvent tromper (JIT n'existe pas en CPython, cache CPU, GC). Utiliser pour **comparer** deux versions, pas pour des conclusions absolues.

## 3. `cProfile` — profil d'un programme entier

```python
import cProfile

cProfile.run("mon_programme()", sort="cumulative")
```

Ou en CLI :

```bash
python -m cProfile -s cumulative mon_script.py
python -m cProfile -o profile.out mon_script.py      # sauvegarde binaire
```

Puis analyse avec `pstats` :

```bash
python -m pstats profile.out
```

Ou visualisation graphique avec [`snakeviz`](https://jiffyclub.github.io/snakeviz/) :

```bash
uv pip install snakeviz
snakeviz profile.out
```

### Colonnes clés

- `ncalls` : nombre d'appels.
- `tottime` : temps passé **directement** dans la fonction (hors sous-appels).
- `cumtime` : temps cumulé (avec sous-appels).

**Focus** : cherchez les fonctions avec un gros `cumtime` au plus près du top. C'est là que se cache le goulot.

## 4. `line_profiler` — profil ligne par ligne

```bash
uv pip install line_profiler
```

Décorez les fonctions à profiler avec `@profile` :

```python
@profile
def ma_fonction():
    data = charger_fichier()       # ligne 1
    for item in data:              # ligne 2
        traiter(item)              # ligne 3
```

Puis :

```bash
kernprof -l -v script.py
```

Sortie :

```
Line #      Hits   Time   Per Hit   % Time  Line Contents
     2         1    5.2      5.2      4.1   data = charger_fichier()
     3         1    0.1      0.1      0.0   for item in data:
     4       100  120.0      1.2     95.8       traiter(item)
```

`line_profiler` révèle LA ligne qui coûte.

## 5. `py-spy` — profilage externe et prod

```bash
uv pip install py-spy
py-spy record -o profile.svg -- python script.py
```

Avantages :
- **S'attache à un process en cours** (par PID) → debugger un serveur en prod.
- Ne nécessite **aucune modification** du code.
- Très faible overhead.

## 6. `memory_profiler` et `tracemalloc`

Pour traquer la consommation mémoire :

```bash
uv pip install memory_profiler
python -m memory_profiler script.py
```

Avec `@profile` sur les fonctions.

`tracemalloc` (stdlib) :

```python
import tracemalloc

tracemalloc.start()

# ... code ...

snapshot = tracemalloc.take_snapshot()
top = snapshot.statistics("lineno")
for stat in top[:10]:
    print(stat)
```

## 7. `__slots__` — revisité

Rappel (Ch. 8) : `__slots__` remplace le `__dict__` d'instance par un tableau fixe.

### Mesure typique

```python
import sys

class A:
    def __init__(self, x, y):
        self.x, self.y = x, y

class B:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y


# ~200+ octets par instance A (objet + __dict__)
# ~50-60 octets par instance B

a = A(1, 2)
b = B(1, 2)
print(sys.getsizeof(a), sys.getsizeof(a.__dict__))   # objet + dict séparé
print(sys.getsizeof(b))                               # objet seul
```

### Quand utiliser

- **Millions d'instances** d'une même classe (ETL, simulations, données).
- Code chaud où l'accès aux attributs doit être rapide.

### Quand ne PAS utiliser

- Classes peu instanciées (gain négligeable).
- Besoin d'attributs dynamiques (`__slots__` le refuse).
- Mix avec dataclasses d'héritage complexe — sauf `@dataclass(slots=True)` direct.

## 8. `weakref` — références faibles

Un `weakref` ne **compte pas** dans le refcount de l'objet. Il permet à l'objet d'être collecté quand plus personne ne le référence fortement.

```python
import weakref

class Big:
    ...

obj = Big()
ref = weakref.ref(obj)

ref()       # → <Big object>
del obj
ref()       # → None (l'objet a été collecté)
```

### Cas d'usage

- **Caches** qui ne doivent pas empêcher le GC : `weakref.WeakValueDictionary`.
- **Observer pattern** sans fuite mémoire.
- **Références circulaires volontaires** (parent ↔ enfant).

```python
from weakref import WeakValueDictionary

cache: WeakValueDictionary[str, Big] = WeakValueDictionary()
cache["k"] = obj
# quand obj n'est plus référencé ailleurs, l'entrée disparaît du cache
```

## 9. Le garbage collector

CPython combine deux stratégies :

1. **Reference counting** : chaque objet sait combien de références pointent vers lui. Quand ça tombe à 0, il est détruit **immédiatement**.
2. **Cyclic GC** : détecte les cycles (A → B → A) que le refcount seul ne peut pas libérer. Tourne périodiquement.

### Contrôler le GC

```python
import gc

gc.disable()        # désactive le cyclic GC (ne désactive PAS le refcount)
gc.enable()
gc.collect()        # force un passage
gc.get_count()      # compteurs des générations
gc.get_stats()
```

### Quand désactiver le GC

Cas rare et précis : **boucle chaude** qui alloue énormément d'objets temporaires mais pas de cycles. Désactiver le GC le temps de la boucle, puis réactiver.

```python
gc.disable()
try:
    for _ in range(1_000_000):
        ...
finally:
    gc.enable()
```

**Ne pas faire à la légère.** Profiler d'abord, confirmer que le GC est le goulot.

## 10. Techniques d'optimisation Python pures

### Préférer les built-ins et structures idiomatiques

```python
# ❌ lent
total = 0
for x in liste:
    total += x

# ✅ rapide, fait en C
total = sum(liste)
```

### Éviter les accès d'attributs dans les boucles chaudes

```python
# Accès d'attribut répété
for item in items:
    self.buffer.append(item)     # self.buffer résolu à chaque itération

# Cache local
append = self.buffer.append
for item in items:
    append(item)                  # accès local, plus rapide
```

Micro-optimisation, mais pertinente dans les boucles numériques.

### Compréhensions > `append` dans une boucle

```python
# ❌
result = []
for x in items:
    result.append(f(x))

# ✅ plus rapide (générées en bytecode optimisé)
result = [f(x) for x in items]
```

### Sets pour l'appartenance

```python
# O(n)
if item in ma_liste: ...

# O(1)
if item in mon_set: ...
```

### Évaluation paresseuse

```python
# ❌ charge tout en mémoire
lines = open("huge.log").readlines()
for line in lines: ...

# ✅ lit ligne par ligne
with open("huge.log") as f:
    for line in f: ...
```

## 11. Quand Python **ne suffit pas**

Si après profilage + optimisation, Python reste trop lent, plusieurs options :

### Vectorisation avec NumPy / pandas

Les opérations se font en C sur des tableaux contigus.

```python
import numpy as np

a = np.arange(1_000_000)
total = (a ** 2).sum()     # 1000x plus rapide que sum(x**2 for x in range(...))
```

### C extensions via Cython / mypyc

`mypyc` (Dropbox) compile du code Python typé en C natif. Très rapide, quasiment sans changer le code :

```bash
uv pip install mypy
mypyc mon_module.py
```

### FFI : ctypes, cffi

Appeler du code C depuis Python.

### Réécrire en Rust + pyo3

`pyo3` permet d'exposer des fonctions Rust comme modules Python. Standard moderne pour les parties critiques (ex. `ruff`, `uv`, `cryptography`).

### Changer d'interpréteur

- **PyPy** : JIT, 5-50× plus rapide pour du code pur Python. Incompatible avec certaines extensions C.
- **Python free-threaded** (3.13+) : désactive le GIL.

## 12. Benchmarks reproductibles avec pytest-benchmark

Pour versionner les perfs et détecter les régressions :

```bash
uv pip install pytest-benchmark
```

```python
def test_tri(benchmark):
    data = list(range(10_000, 0, -1))
    result = benchmark(sorted, data)
    assert result[0] == 1
```

`pytest` affiche min/max/mean, vous alerte si une régression dépasse un seuil.

---

### Piège courant : "optimiser" sans mesurer

```python
# Quelqu'un sur Stack Overflow dit que X est plus rapide que Y. On change.
# → Changement cosmétique, gain nul ou négatif.
```

Toujours mesurer **avant** et **après**, **sur vos données réelles**.

---

### Sous le capot : les entiers sont des objets

Chaque `int` en Python est un objet (environ 28 octets pour les petits entiers). Une liste de 1 million d'ints consomme ~28 Mo **juste pour les ints** — sans compter les pointeurs de la liste.

Pour du gros volume numérique : `numpy.ndarray` ou `array.array` stockent des int/float compacts comme en C. **50x** moins de mémoire.

---

## À retenir

- Mesurer avant d'optimiser. Toujours.
- `timeit` pour micro, `cProfile` + snakeviz pour macro, `line_profiler` pour la ligne.
- `py-spy` pour prod.
- `__slots__` et `@dataclass(slots=True)` quand on crée **beaucoup** d'instances.
- Préférer built-ins (`sum`, `map`, compréhensions).
- Sets pour le test d'appartenance, générateurs pour les flux.
- Si Python n'y suffit pas : NumPy, Cython/mypyc, Rust/pyo3.
- Benchmarks versionnés avec `pytest-benchmark`.

---

➡️ [Chapitre 15 — Dev web moderne avec FastAPI](../15_dev_web/README.md)
