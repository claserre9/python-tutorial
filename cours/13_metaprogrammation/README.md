# Chapitre 13 — Métaprogrammation & introspection

**Écrire du code qui manipule du code**. Modifier des classes à leur création, inspecter les objets à l'exécution, lire leurs annotations. Sujet fascinant, **à utiliser avec parcimonie** : la métaprogrammation est puissante mais rend les choses opaques.

## 1. `type` — la classe des classes

`type` a un double rôle :

```python
type(42)        # <class 'int'>  — le TYPE d'une valeur
type(int)       # <class 'type'> — LE type des classes
```

Les classes sont des **objets**. Leur type est `type`. `type` est donc la **métaclasse par défaut**.

### `type(name, bases, dict)` — créer une classe dynamiquement

```python
# Équivalent :
class Personne:
    espece = "humain"
    def saluer(self):
        return f"bonjour, je suis {self.nom}"


Personne = type("Personne", (), {
    "espece": "humain",
    "saluer": lambda self: f"bonjour, je suis {self.nom}",
})
```

Les deux sont strictement équivalents : `class` est du sucre syntaxique pour `type()`.

## 2. Introspection

### `dir(obj)` — lister les attributs

```python
class C:
    x = 1
    def m(self): ...

dir(C)
# ['__class__', '__delattr__', ..., 'm', 'x']
```

### `getattr`, `setattr`, `hasattr`, `delattr`

```python
getattr(obj, "x")                       # obj.x
getattr(obj, "x", "default")            # défaut si absent
setattr(obj, "x", 42)                   # obj.x = 42
hasattr(obj, "x")                       # True / False
delattr(obj, "x")                       # del obj.x
```

Utile quand le nom de l'attribut est dynamique :

```python
for champ, valeur in user_input.items():
    setattr(user, champ, valeur)
```

### `vars(obj)` — `__dict__` lisible

```python
vars(obj)            # équivalent à obj.__dict__
```

### `__class__`, `__bases__`, `__mro__`

```python
obj.__class__        # classe de l'instance (équivalent à type(obj))
C.__bases__          # tuple des parents directs
C.__mro__            # ordre de résolution des méthodes
C.__subclasses__()   # sous-classes directes
```

## 3. `inspect` — introspection avancée

```python
import inspect


def ma_fonction(a: int, b: str = "x") -> bool: ...


sig = inspect.signature(ma_fonction)
sig                           # (a: int, b: str = 'x') -> bool
sig.parameters                # {'a': <Parameter 'a: int'>, 'b': ...}
sig.return_annotation         # <class 'bool'>

for name, param in sig.parameters.items():
    param.name
    param.annotation
    param.default
    param.kind      # POSITIONAL_OR_KEYWORD, KEYWORD_ONLY, VAR_POSITIONAL, ...
```

### Autres fonctions utiles

```python
inspect.isclass(x)
inspect.isfunction(x)
inspect.iscoroutinefunction(x)
inspect.getsource(f)           # code source
inspect.getmembers(obj)        # liste (name, value)
inspect.stack()                # pile d'appels
```

Utilisé par FastAPI pour générer OpenAPI, par pytest pour détecter les fixtures, etc.

## 4. Annotations à l'exécution

### `__annotations__`

```python
def f(x: int, y: str = "x") -> bool: ...
f.__annotations__              # {'x': int, 'y': str, 'return': bool}


class C:
    x: int
    y: str = "default"

C.__annotations__              # {'x': int, 'y': str}
```

### `get_type_hints` — résolution des forward refs

```python
from typing import get_type_hints

class C:
    x: "C"           # forward ref

get_type_hints(C)    # {'x': <class 'C'>}  ← résolu
```

Toujours préférer `get_type_hints()` à `__annotations__` pour lire des types utilisables.

## 5. `__init_subclass__` — alternative moderne aux métaclasses

Pour réagir à la création d'une sous-classe **sans métaclasse** :

```python
class Plugin:
    REGISTRY: dict[str, type["Plugin"]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.REGISTRY[cls.__name__] = cls


class PluginA(Plugin): ...
class PluginB(Plugin): ...


Plugin.REGISTRY      # {'PluginA': PluginA, 'PluginB': PluginB}
```

Excellent pour les registries, les checks de cohérence, la configuration. Avant Python 3.6, c'était le travail d'une métaclasse.

### Avec des paramètres

```python
class Tagged:
    def __init_subclass__(cls, *, tag: str, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.tag = tag


class Foo(Tagged, tag="foo"):
    pass


Foo.tag    # "foo"
```

## 6. Métaclasses — quand `__init_subclass__` ne suffit pas

Une métaclasse est une classe **dont les instances sont des classes**. Son `__new__`/`__init__` est appelé à la création de la classe.

```python
class Registre(type):
    REGISTRY: dict[str, type] = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        Registre.REGISTRY[name] = cls
        return cls


class A(metaclass=Registre): ...
class B(metaclass=Registre): ...


Registre.REGISTRY      # {'A': A, 'B': B}
```

Cas d'usage **légitimes** (rares) :

- Interdire la création de certaines classes.
- Modifier **profondément** la classe (ex. ORMs Django/SQLAlchemy, Pydantic v1).
- Implémenter des DSL.

### Pourquoi c'est piégeux

Les métaclasses **traversent** l'héritage. Si une classe A a une métaclasse `M1` et B une métaclasse `M2`, une sous-classe de `A` et `B` doit avoir une métaclasse compatible (souvent impossible).

**Règle** : 99% des cas couverts par `__init_subclass__`, décorateurs de classe, ou dataclasses. Une métaclasse custom est un choix de dernier recours.

## 7. Monkey-patching

Modifier dynamiquement du code qu'on ne contrôle pas :

```python
import requests

original_get = requests.get

def get_avec_log(*args, **kwargs):
    print(f"GET {args[0]}")
    return original_get(*args, **kwargs)

requests.get = get_avec_log
```

### Cas légitime : les tests

```python
# Via monkeypatch de pytest
def test_foo(monkeypatch):
    monkeypatch.setattr("mon_module.clock", lambda: 123)
    ...
```

### Cas dangereux : modifier une lib en prod

Écrase le comportement pour **tout le process**. Mauvaise maintenabilité, bugs traçables très difficilement.

## 8. `__getattr__` et `__getattribute__`

Permet d'intercepter **dynamiquement** les accès d'attribut.

```python
class Proxy:
    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        # Appelé UNIQUEMENT si l'attribut n'existe pas normalement
        return getattr(self._target, name)


p = Proxy({"a": 1})
p.keys()           # appelle __getattr__ → dict.keys
```

- `__getattr__(self, name)` : appelé en **dernier recours** (attribut absent).
- `__getattribute__(self, name)` : appelé **systématiquement** pour tout accès. Dangereux — modifiez `__getattr__` sauf si vraiment nécessaire.

### Cas d'usage

- **Proxy / wrapper** : retransmettre les appels à un objet interne.
- **Lazy loading** : charger une valeur la première fois qu'elle est demandée.
- **ORM** : exposer les colonnes d'une table comme attributs.

## 9. `__getattr__` au niveau module (PEP 562)

Depuis 3.7 :

```python
# mon_module.py
def __getattr__(name):
    if name == "VALEUR_COUTEUSE":
        return calcul_long()
    raise AttributeError(f"module has no attribute {name!r}")
```

Utilisé pour les dépréciations :

```python
def __getattr__(name):
    if name == "ancienne_fn":
        import warnings
        warnings.warn("ancienne_fn est dépréciée, utilisez nouvelle_fn", DeprecationWarning)
        return nouvelle_fn
    raise AttributeError(...)
```

---

### Piège courant : conflit de métaclasses

```python
class M1(type): ...
class M2(type): ...

class A(metaclass=M1): ...
class B(metaclass=M2): ...

class C(A, B):    # ❌ TypeError: metaclass conflict
    ...
```

Il faut créer une métaclasse `M3(M1, M2)` compatible. Dans 99% des cas, c'est le signe qu'on utilise les métaclasses à mauvais escient.

---

### Sous le capot : comment Python crée une classe

Quand Python voit `class C(A, B):`, il fait :

1. Détermine la métaclasse (`type` par défaut, ou `metaclass=...`, ou celle d'un parent).
2. Appelle `meta.__prepare__(name, bases)` → retourne le namespace (dict vide d'ordinaire).
3. Exécute le corps de la classe dans ce namespace.
4. Appelle `meta(name, bases, namespace)` → crée la classe.

Connaître ce flux permet de débugger les soucis exotiques (metaclass conflict, ordre d'exécution, `__class_getitem__`...).

---

## À retenir

- Les classes sont des objets. `type` est leur métaclasse.
- `getattr` / `setattr` / `hasattr` pour les accès dynamiques.
- `inspect.signature` pour lire une signature, `get_type_hints` pour les annotations.
- `__init_subclass__` remplace la plupart des métaclasses.
- Monkey-patching : OK pour les tests, risqué en prod.
- `__getattr__` module : pour lazy loading et dépréciations.
- Métaprogrammation puissante ≠ appropriée : préférez toujours le code explicite.

---

➡️ [Chapitre 14 — Performance & internals CPython](../14_performance/README.md)
