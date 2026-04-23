# Chapitre 11 — Décorateurs & descripteurs

Les décorateurs sont **omniprésents** en Python moderne (`@dataclass`, `@property`, `@pytest.fixture`, `@app.get`). Ce chapitre va au-delà du "un décorateur c'est @truc" : décorateurs paramétrés, typés, empilés, de classes. Puis **descripteurs** — le mécanisme bas niveau qui explique comment `@property` fonctionne.

## 1. Rappel : fonctions de première classe

(Vu au Ch. 4, mais c'est la fondation des décorateurs.)

Une fonction peut être passée, retournée, stockée. Une fonction qui **prend une fonction** et **retourne une fonction** s'appelle une **fonction d'ordre supérieur** (higher-order function).

## 2. Décorateur basique

```python
def trace(fn):
    def wrapper(*args, **kwargs):
        print(f"→ {fn.__name__}({args}, {kwargs})")
        result = fn(*args, **kwargs)
        print(f"← {fn.__name__} → {result}")
        return result
    return wrapper


@trace
def additionner(a, b):
    return a + b


additionner(3, 4)
# → additionner((3, 4), {})
# ← additionner → 7
```

La syntaxe `@trace` est sucre pour :

```python
def additionner(a, b): ...
additionner = trace(additionner)
```

## 3. `functools.wraps` — indispensable

Sans précaution, le décorateur **écrase** les métadonnées :

```python
@trace
def additionner(a, b):
    """Addition."""
    return a + b


additionner.__name__     # 'wrapper' (écrasé !)
additionner.__doc__      # None
help(additionner)        # affiche wrapper, pas additionner
```

Correction avec `@functools.wraps` :

```python
from functools import wraps

def trace(fn):
    @wraps(fn)              # copie __name__, __doc__, __wrapped__, __module__, ...
    def wrapper(*args, **kwargs):
        ...
        return fn(*args, **kwargs)
    return wrapper
```

**Règle absolue** : tout décorateur doit utiliser `@wraps(fn)`.

## 4. Décorateurs paramétrés

Parfois on veut `@retry(times=3)` ou `@cache(maxsize=128)`. Il faut ajouter un niveau : une **fabrique de décorateur**.

```python
from functools import wraps

def retry(times: int = 3):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for tentative in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    if tentative == times:
                        raise
                    print(f"échec #{tentative} : {e}, retry")
        return wrapper
    return decorator


@retry(times=5)
def appel_flaky():
    ...
```

Structure à trois niveaux :
- `retry(times=5)` : fabrique, retourne `decorator`
- `decorator(fn)` : décorateur, retourne `wrapper`
- `wrapper(*args, **kwargs)` : appelé à la place de `fn`

### Supporter à la fois `@deco` et `@deco(...)`

```python
def mon_deco(fn=None, *, param=None):
    if fn is None:
        return lambda f: mon_deco(f, param=param)

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # ...
        return fn(*args, **kwargs)
    return wrapper


@mon_deco
def f(): ...

@mon_deco(param=5)
def g(): ...
```

Pattern utilisé par `@dataclass` et d'autres.

## 5. Décorateurs typés (PEP 612)

Un décorateur qui ne change **pas la signature** doit la préserver pour mypy/IDE. Utilisez `ParamSpec` :

```python
from functools import wraps
from typing import ParamSpec, TypeVar, Callable

P = ParamSpec("P")
R = TypeVar("R")


def trace(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"→ {fn.__name__}")
        result = fn(*args, **kwargs)
        print(f"← {fn.__name__}")
        return result
    return wrapper


@trace
def additionner(a: int, b: int) -> int:
    return a + b


additionner(3, 4)           # mypy : retourne int, accepte (int, int)
additionner("a", 1)         # mypy : ERROR
```

Sans `ParamSpec`, mypy aurait typé `additionner` comme `Callable[..., int]` — perte de la signature.

## 6. Empiler les décorateurs

```python
@trace
@cache
def f(x): ...
```

Équivalent à : `f = trace(cache(f))`. L'ordre **compte** :

- Exécution : `trace` s'applique AUTOUR du cache. Log avant/après la consultation du cache.
- Si inversé `@cache / @trace` : cache autour, log juste avant/après le vrai calcul.

Règle : lire de bas en haut pour savoir qui enveloppe qui.

## 7. Décorateurs de classe

Un décorateur peut aussi s'appliquer à une classe :

```python
def register(cls):
    REGISTRY[cls.__name__] = cls
    return cls


@register
class Plugin:
    ...
```

C'est ainsi que `@dataclass` fonctionne : il **modifie la classe** (génère `__init__`, `__repr__`, etc.) puis la renvoie.

### Décorateur de classe paramétré

```python
def singleton(cls):
    instances = {}
    @wraps(cls, updated=())
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class Config: ...


Config() is Config()       # True
```

## 8. Cas d'usage réels

### Mesure de temps

```python
import time
from functools import wraps

def timed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} : {time.perf_counter() - t0:.3f}s")
        return result
    return wrapper
```

### Validation d'arguments

```python
def valide_positif(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        for v in args:
            if isinstance(v, (int, float)) and v < 0:
                raise ValueError(f"argument négatif : {v}")
        return fn(*args, **kwargs)
    return wrapper
```

### Logging structuré

```python
def log_call(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        logger.info("call", extra={"fn": fn.__name__, "args": args})
        try:
            return fn(*args, **kwargs)
        except Exception:
            logger.exception("failed", extra={"fn": fn.__name__})
            raise
    return wrapper
```

---

## 9. Descripteurs — le mécanisme derrière `@property`

Un **descripteur** est un objet qui implémente un ou plusieurs de : `__get__`, `__set__`, `__delete__`. Quand cet objet est **attribut d'une classe**, Python déclenche ces méthodes à la lecture/écriture/suppression.

C'est le protocole qui explique `@property`, `@classmethod`, `@staticmethod`, les méthodes, et même les attributs d'instance via `__dict__`.

### Exemple minimal

```python
class TypedField:
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __set_name__(self, owner, name):        # 3.6+ : reçoit le nom de l'attribut
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name}: attendu {self.expected_type.__name__}")
        instance.__dict__[self.name] = value


class Personne:
    nom = TypedField(str)
    age = TypedField(int)


p = Personne()
p.nom = "Alice"     # OK
p.age = "trente"    # TypeError: age: attendu int
```

### Comment ça marche

Quand vous écrivez `p.nom = "Alice"` :

1. Python trouve `nom` dans `type(p).__dict__` (la classe).
2. `nom` est un objet `TypedField`, **avec** `__set__`.
3. Python appelle `TypedField.__set__(nom, p, "Alice")`.

Si on lisait `p.nom`, Python appelle `TypedField.__get__(nom, p, Personne)`.

### Data descriptor vs non-data descriptor

| | Définit | Précédence |
|---|---|---|
| Data descriptor | `__set__` (et/ou `__delete__`) | prend le pas sur `__dict__` d'instance |
| Non-data descriptor | juste `__get__` | le `__dict__` d'instance gagne |

Conséquence pratique : un **data descriptor** ne peut pas être "écrasé" par une simple assignation `self.x = ...`. C'est ce qui rend `@property` inshadowable.

### `@property` sous forme de descripteur

```python
# Ceci :
class C:
    @property
    def nom(self): return self._nom

    @nom.setter
    def nom(self, v): self._nom = v


# Équivaut à :
class C:
    def _get_nom(self): return self._nom
    def _set_nom(self, v): self._nom = v
    nom = property(fget=_get_nom, fset=_set_nom)
```

`property` est un **data descriptor** built-in qui encapsule les getter/setter. Mystère résolu.

### Cas d'usage des descripteurs personnalisés

- **Validation typée réutilisable** (comme `TypedField` ci-dessus). Permet d'éviter de dupliquer `@property` partout.
- **ORMs** : `django.db.models.CharField(...)`, `sqlalchemy.Column(...)` sont des descripteurs.
- **Lazy loading** : calculer une valeur au premier accès, la cacher ensuite.
- **Attributs calculés avec dépendances**.

### Exemple : `lazy_property` — calcul différé + cache

```python
class lazy_property:
    def __init__(self, fn):
        self.fn = fn
        self.name = fn.__name__

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        val = self.fn(instance)
        instance.__dict__[self.name] = val    # écrase le descripteur pour cet instance
        return val


class Rapport:
    def __init__(self, data):
        self.data = data

    @lazy_property
    def statistiques(self):
        print("calcul...")
        return expensive_compute(self.data)


r = Rapport([1, 2, 3])
r.statistiques          # 'calcul...' + résultat
r.statistiques          # pas de recalcul
```

**Astuce** : `lazy_property` est un **non-data descriptor** (pas de `__set__`), donc `__dict__` d'instance le masque après le premier accès. C'est ce qui implémente le cache.

---

### Piège courant : décorateur qui ne passe pas ses arguments

```python
def compteur(fn):
    n = 0
    @wraps(fn)
    def wrapper():        # ❌ ne prend ni *args ni **kwargs
        nonlocal n
        n += 1
        return fn()
    return wrapper


@compteur
def additionner(a, b): ...

additionner(1, 2)         # TypeError: wrapper() takes 0 positional arguments
```

**Règle** : un wrapper générique doit presque toujours accepter `*args, **kwargs`.

---

### Sous le capot : ordre de lookup d'attribut

Pour `obj.attr`, Python fait **approximativement** :

1. Cherche `attr` dans `type(obj).__mro__`. Si trouvé et c'est un **data descriptor**, appelle `__get__`.
2. Sinon, cherche dans `obj.__dict__`. Si trouvé, retourne.
3. Sinon, retour au MRO : si c'est un **non-data descriptor**, `__get__`. Sinon, retourne tel quel.
4. Sinon `__getattr__` (si défini), sinon `AttributeError`.

C'est pourquoi `@property` (data descriptor) ne peut pas être masqué par une assignation d'instance, mais une méthode ordinaire (fonction, donc non-data descriptor) peut être "écrasée" sur une instance particulière.

---

## À retenir

- Tout décorateur : `@functools.wraps(fn)`.
- Décorateur paramétré = trois niveaux (fabrique → decorator → wrapper).
- Type proprement les décorateurs avec `ParamSpec`.
- L'ordre des décorateurs empilés compte : lire de bas en haut.
- Un descripteur implémente `__get__` / `__set__` / `__delete__` et s'active quand il est attribut de classe.
- `@property` = data descriptor built-in.
- Data descriptor > `__dict__` d'instance > non-data descriptor (précédence de lookup).

---

➡️ [Chapitre 12 — Concurrence & async](../12_concurrence/README.md)
