# Chapitre 8 — POO avancée

Héritage simple et multiple, **MRO** (Method Resolution Order), `super()` coopératif, composition vs héritage, `ABC` vs `Protocol`, `__slots__`. Les sujets que les tutos superficiels évitent, et qui font la différence entre "je connais la syntaxe" et "je conçois des systèmes maintenables".

## 1. Héritage simple

```python
class Animal:
    def __init__(self, nom: str):
        self.nom = nom

    def parler(self) -> str:
        return "..."


class Chien(Animal):
    def parler(self) -> str:           # override
        return "Woof"
```

- `Chien` **hérite** de tous les attributs et méthodes d'`Animal`.
- Il **redéfinit** (override) `parler`.
- `isinstance(Chien("Rex"), Animal)` est `True`.

### `super()` — appeler la version parente

```python
class Animal:
    def __init__(self, nom: str):
        self.nom = nom

    def __repr__(self):
        return f"Animal({self.nom})"


class Chien(Animal):
    def __init__(self, nom: str, race: str):
        super().__init__(nom)          # appelle Animal.__init__
        self.race = race

    def __repr__(self):
        return super().__repr__() + f"[{self.race}]"


Chien("Rex", "labrador")               # Animal(Rex)[labrador]
```

**Ne pas faire** : `Animal.__init__(self, nom)`. Ça marche pour l'héritage simple mais casse l'héritage multiple. Toujours `super()`.

## 2. Héritage multiple et **MRO** (C3 linearization)

Python autorise l'héritage multiple. La question : quand deux parents ont la même méthode, laquelle est appelée ?

```python
class A:
    def greet(self): return "A"

class B(A):
    def greet(self): return "B"

class C(A):
    def greet(self): return "C"

class D(B, C):
    pass


D().greet()           # 'B' — mais pourquoi ?
D.__mro__             # (D, B, C, A, object)
```

Le **MRO** est l'ordre dans lequel Python cherche les méthodes. Calculé par l'algorithme **C3 linearization**. Règles principales :

1. La classe elle-même d'abord.
2. Les parents dans l'ordre de déclaration.
3. Un parent n'est visité qu'après toutes ses sous-classes.

Pour un MRO impossible à calculer, Python lève `TypeError`. Inspecter avec `Classe.__mro__` ou `Classe.mro()`.

### `super()` en héritage multiple : héritage coopératif

```python
class A:
    def __init__(self):
        print("A")
        super().__init__()       # ← même dans A !

class B(A):
    def __init__(self):
        print("B")
        super().__init__()

class C(A):
    def __init__(self):
        print("C")
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D")
        super().__init__()


D()
# Affiche :
# D
# B
# C
# A
```

`super()` dans `B.__init__` n'appelle pas forcément `A.__init__` ! Il appelle **la classe suivante dans le MRO de l'instance**. Ici, dans le contexte `D()`, c'est `C`.

C'est l'**héritage coopératif** : chaque classe appelle `super()` sans présumer qui est derrière. Fonctionne uniquement si **toutes** les classes le font (d'où le `super().__init__()` même dans `A`).

### Le classique "diamond" (diamant)

```
    A
   / \
  B   C
   \ /
    D
```

Sans MRO, `A.__init__` serait appelée deux fois (une fois par `B`, une fois par `C`). Le MRO linéarise la hiérarchie pour que chaque classe ne soit visitée qu'une fois.

## 3. Polymorphisme et duck typing

Python n'exige pas qu'un objet hérite d'un type pour être utilisé comme tel. Si un objet a la méthode `parler()`, il peut être utilisé là où on attend "quelque chose qui parle".

```python
class Chat:
    def parler(self): return "Miaou"

class Duck:
    def parler(self): return "Coin"


def faire_parler(animal):
    return animal.parler()


faire_parler(Chat())    # 'Miaou'
faire_parler(Duck())    # 'Coin'
```

**"If it walks like a duck and quacks like a duck, it's a duck."**

Inconvénient : pas vérifié statiquement. Solution : `Protocol` (§6).

## 4. Composition > héritage (souvent)

L'héritage "est un" (`Chien est un Animal`) a deux défauts :

- **Couplage fort** : modifier le parent casse les enfants.
- **Abus fréquent** : on hérite pour "gagner les méthodes", pas parce que c'est sémantiquement juste.

La **composition** ("a un") est souvent meilleure.

```python
# ❌ Héritage abusif
class Email(SMTPClient):         # un email n'EST PAS un client SMTP
    ...

# ✅ Composition
class Email:
    def __init__(self, smtp: SMTPClient):
        self.smtp = smtp                # un email A un client pour s'envoyer
```

**Heuristique** : si vous hésitez, commencez par composition. Vous pouvez toujours extraire une classe de base plus tard.

## 5. Classes abstraites (`ABC`)

Pour **imposer** qu'un sous-classe implémente certaines méthodes :

```python
from abc import ABC, abstractmethod


class Forme(ABC):
    @abstractmethod
    def aire(self) -> float: ...

    @abstractmethod
    def perimetre(self) -> float: ...


class Rectangle(Forme):
    def __init__(self, l, h):
        self.l, self.h = l, h

    def aire(self):
        return self.l * self.h

    def perimetre(self):
        return 2 * (self.l + self.h)


Forme()        # ❌ TypeError: can't instantiate abstract class
Rectangle(3, 4).aire()   # 12
```

- `ABC` est la classe de base abstraite.
- `@abstractmethod` marque une méthode obligatoire.
- Impossible d'instancier tant qu'une méthode abstraite reste.

### Typage nominal vs structural

`ABC` impose une relation **nominale** : vous devez **hériter** de `Forme` pour en être une. C'est comme les interfaces Java.

Pour une approche **structurelle** (duck typing typé), utilisez `Protocol`.

## 6. `Protocol` — typage structurel (PEP 544)

```python
from typing import Protocol


class Parlant(Protocol):
    def parler(self) -> str: ...


def faire_parler(animal: Parlant) -> str:
    return animal.parler()


class Chat:
    def parler(self): return "Miaou"


faire_parler(Chat())      # OK pour mypy, sans que Chat n'hérite de Parlant
```

`Chat` n'hérite pas de `Parlant` mais **est** un `Parlant` parce qu'il a la bonne forme. C'est du duck typing vérifiable statiquement.

### `@runtime_checkable`

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Parlant(Protocol):
    def parler(self) -> str: ...


isinstance(Chat(), Parlant)    # True
```

Permet `isinstance()` au runtime. À utiliser avec parcimonie (vérifie juste l'existence des méthodes, pas leurs signatures).

### `ABC` vs `Protocol` — quand utiliser quoi ?

| | `ABC` | `Protocol` |
|---|---|---|
| Relation | nominale (héritage obligatoire) | structurelle (forme) |
| Vérification | runtime ET mypy | mypy surtout |
| Partage de code | oui (peut avoir des méthodes concrètes) | non (contrat pur) |
| Usage typique | hiérarchies métier (`Forme`, `Paiement`) | interfaces techniques (`SupportsRead`, `Parlant`) |

Règle : pour un contrat d'API entre modules, `Protocol`. Pour une hiérarchie métier avec comportement partagé, `ABC`.

## 7. `__slots__` — perf mémoire

Par défaut, chaque instance a un `__dict__` qui stocke ses attributs dynamiquement. C'est flexible mais **coûteux** : ~200-300 octets par instance même pour 2 attributs.

`__slots__` déclare les attributs à l'avance, remplace le `__dict__` par un tableau fixe :

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y
```

Gain : ~40-60% de mémoire, accès ~10% plus rapide. Critique avec **millions d'instances**.

### Contraintes

- Pas de création dynamique d'attributs (`p.z = 3` → `AttributeError`).
- Pas de `__dict__` (sauf si `"__dict__"` ajouté dans `__slots__`).
- Héritage : les sous-classes doivent aussi déclarer `__slots__` pour en bénéficier.

### Avec dataclass

```python
@dataclass(slots=True)            # 3.10+
class Point:
    x: float
    y: float
```

`@dataclass(slots=True)` génère `__slots__` automatiquement. **Excellent défaut** pour les value objects.

## 8. Pattern : interface + implémentations

Cas d'usage classique.

```python
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def envoyer(self, destinataire: str, message: str) -> None: ...


class EmailNotifier(Notifier):
    def envoyer(self, destinataire, message):
        # ... SMTP
        print(f"EMAIL → {destinataire}: {message}")


class SMSNotifier(Notifier):
    def envoyer(self, destinataire, message):
        # ... Twilio
        print(f"SMS → {destinataire}: {message}")


class Service:
    def __init__(self, notifier: Notifier):   # injection de dépendance
        self.notifier = notifier

    def alerter(self, user, msg):
        self.notifier.envoyer(user, msg)


# Échangeable à l'exécution :
Service(EmailNotifier()).alerter("a@b", "ping")
Service(SMSNotifier()).alerter("+33...", "ping")
```

Bénéfice : testable (fake notifier dans les tests), extensible (ajouter `SlackNotifier` sans toucher à `Service`).

## 9. `@dataclass` et héritage — piège

```python
@dataclass
class Base:
    x: int

@dataclass
class Derived(Base):
    y: int = 0       # ❌ TypeError : champ avec défaut suivi d'un sans défaut ?
```

Si `Base.x` n'a pas de défaut et `Derived.y` non plus, ça marche. Mais dès qu'un champ avec défaut précède un sans défaut dans l'ordre final, échec.

**Solution** : `kw_only=True` (3.10+), qui supprime la contrainte d'ordre.

```python
@dataclass(kw_only=True)
class Base:
    x: int

@dataclass(kw_only=True)
class Derived(Base):
    y: int = 0        # ✅
```

Raison de plus d'utiliser `kw_only=True` par défaut.

---

### Piège courant : mutable shared state entre sous-classes

```python
class Entity:
    tags = []              # ❌ attribut de classe, partagé par TOUTES les sous-classes


class User(Entity):
    pass


User.tags.append("actif")
print(Entity.tags)         # ['actif'] ← pollution remontée
```

Toujours initialiser dans `__init__`, ou utiliser `field(default_factory=list)` dans une dataclass.

---

### Sous le capot : `super()` sans arguments

```python
class A:
    def __init__(self):
        super().__init__()    # équivalent à super(A, self).__init__()
```

Le compilateur Python injecte automatiquement la classe et l'instance. C'est de la "compiler magic" (via une cellule dans le scope).

`super(Classe, instance)` explicite est parfois utile pour naviguer manuellement le MRO (rare).

---

## À retenir

- `super()` **toujours**, même en héritage simple.
- En héritage multiple, toutes les classes doivent appeler `super()` pour l'héritage coopératif.
- `Classe.__mro__` pour inspecter l'ordre de résolution.
- Composition > héritage dans le doute.
- `ABC` pour hiérarchies métier, `Protocol` pour interfaces techniques.
- `@dataclass(slots=True)` = très bon défaut pour les value objects.
- `kw_only=True` évite les pièges d'ordre en héritage de dataclasses.

---

➡️ [Chapitre 9 — Itérateurs, générateurs, fonctionnel](../09_concepts_experts/README.md)
