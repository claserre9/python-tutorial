# Chapitre 7 — POO : bases solides

Classes, instances, attributs, méthodes. Les bases. Mais avec les subtilités que les tutos superficiels évitent : attribut de classe vs d'instance (source n°1 de bugs), différence entre `@staticmethod` et `@classmethod`, les dunders qui comptent, et surtout les **dataclasses** (à privilégier dans 90% des cas).

## 1. Classe, instance, attribut

```python
class Chien:
    espece = "Canis familiaris"      # attribut de CLASSE, partagé

    def __init__(self, nom: str):
        self.nom = nom               # attribut d'INSTANCE, propre

    def aboyer(self) -> str:
        return f"{self.nom} dit : Woof !"


rex = Chien("Rex")
rex.nom                # 'Rex'
rex.espece             # 'Canis familiaris' (trouvé sur la classe)
Chien.espece           # 'Canis familiaris'
```

- **`__init__`** : pas un "constructeur" au sens C++/Java. L'objet est **déjà** construit par `__new__` avant que `__init__` ne soit appelé. On verra `__new__` au Ch. 13.
- **`self`** : référence à l'instance courante. N'est pas un mot-clé, juste une convention.

### Attribut de classe vs d'instance — le piège

```python
class Panier:
    articles = []                 # ❌ PIÈGE : partagé entre TOUTES les instances

    def ajouter(self, item):
        self.articles.append(item)


p1 = Panier()
p2 = Panier()
p1.ajouter("pomme")
print(p2.articles)               # ['pomme'] ← catastrophe
```

**Correction** : initialiser dans `__init__` :

```python
class Panier:
    def __init__(self):
        self.articles = []        # ✅ chaque instance a sa propre liste
```

Règle : **attributs de classe = valeurs immuables** (constantes, config). Pour tout ce qui est mutable (list, dict, set), initialiser dans `__init__`.

## 2. Méthodes : d'instance, de classe, statiques

```python
class Cercle:
    PI = 3.14159

    def __init__(self, rayon: float):
        self.rayon = rayon

    # Méthode d'instance : reçoit self
    def surface(self) -> float:
        return self.PI * self.rayon ** 2

    # Méthode de CLASSE : reçoit la classe, pas l'instance
    @classmethod
    def unite(cls) -> "Cercle":
        return cls(rayon=1)               # factory alternative

    # Méthode STATIQUE : ni self ni cls
    @staticmethod
    def pi_sur_deux() -> float:
        return Cercle.PI / 2
```

### Quand utiliser quoi

| | Reçoit | Utilisation |
|---|---|---|
| Méthode d'instance | `self` | agit sur l'état de l'objet |
| `@classmethod` | `cls` | factory alternative, accès à la classe (héritage-friendly) |
| `@staticmethod` | rien | fonction logiquement liée à la classe mais indépendante de l'état |

### Factory via `@classmethod` — pattern courant

```python
class Date:
    def __init__(self, jour: int, mois: int, annee: int):
        self.jour = jour
        self.mois = mois
        self.annee = annee

    @classmethod
    def from_string(cls, s: str) -> "Date":
        j, m, a = map(int, s.split("-"))
        return cls(j, m, a)              # cls, pas Date : fonctionne avec sous-classes


d = Date.from_string("15-03-2026")
```

Pourquoi `cls` et pas `Date` ? Si quelqu'un crée `class DateFr(Date):`, alors `DateFr.from_string(...)` doit retourner un `DateFr`, pas un `Date`. `cls` gère ça automatiquement.

## 3. Dunder methods (méthodes spéciales)

Python offre un protocole de "méthodes magiques" entourées de `__` qui contrôlent le comportement des opérateurs et built-ins.

### `__init__`, `__repr__`, `__str__`

```python
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Représentation non ambiguë, pour les devs. Doit être valide Python si possible."""
        return f"Point(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        """Représentation lisible, pour les utilisateurs."""
        return f"({self.x}, {self.y})"


p = Point(3, 4)
print(p)              # utilise __str__ → '(3, 4)'
repr(p)               # '__repr__' → 'Point(x=3, y=4)'
[p, p]                # utilise __repr__ → '[Point(x=3, y=4), Point(x=3, y=4)]'
```

**Règle** : toujours implémenter `__repr__`. `__str__` est optionnel (tombe sur `__repr__` si absent).

Un bon `__repr__` doit permettre de reconstruire l'objet : `eval(repr(obj)) == obj` est l'idéal.

### `__eq__` et `__hash__`

Par défaut, l'égalité est l'identité (`a == b` ⇔ `a is b`). Pour une égalité structurelle :

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))
```

**Règle critique** : si vous redéfinissez `__eq__`, vous **devez** redéfinir `__hash__` (ou mettre `__hash__ = None` pour empêcher le hash). Deux objets égaux doivent avoir le même hash. Sinon, `dict` et `set` casseront.

Retourner `NotImplemented` (pas `NotImplementedError`) permet à Python de tester la réciproque (`other.__eq__(self)`).

### `__lt__`, `__le__`, etc. (ordre)

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major, minor):
        self.major, self.minor = major, minor

    def __eq__(self, other):
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        return (self.major, self.minor) < (other.major, other.minor)
```

`@total_ordering` génère `__le__`, `__gt__`, `__ge__` à partir de `__eq__` + `__lt__`. Évite les oublis.

### Autres dunders utiles

| Dunder | Opérateur / built-in | Exemple |
|---|---|---|
| `__len__` | `len(obj)` | taille |
| `__contains__` | `x in obj` | appartenance |
| `__iter__` | `for x in obj` | itération (Ch. 9) |
| `__getitem__` | `obj[i]` | indexation |
| `__setitem__` | `obj[i] = v` | assignation |
| `__call__` | `obj()` | rendre appelable |
| `__add__`, `__sub__`... | `+`, `-`... | opérateurs arithmétiques |
| `__bool__` | `bool(obj)` | truthiness |

Liste complète : [docs.python.org/reference/datamodel](https://docs.python.org/3/reference/datamodel.html).

## 4. Les **dataclasses** : à privilégier

Écrire `__init__`, `__repr__`, `__eq__` à la main est répétitif. Depuis Python 3.7, `@dataclass` génère tout ça.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

Équivalent à :

```python
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented
```

### Options importantes

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class User:
    id: int
    nom: str
    tags: list[str] = field(default_factory=list)
    email: str | None = None
```

| Option | Effet |
|---|---|
| `frozen=True` | instance immuable ; rend la classe **hashable** automatiquement |
| `slots=True` (3.10+) | utilise `__slots__` : plus léger en mémoire, pas de nouveaux attributs dynamiques |
| `kw_only=True` (3.10+) | tous les champs sont keyword-only (pas de `User(1, "Alice")`) |
| `order=True` | génère `__lt__`, `__le__`, etc. (compare comme un tuple des champs) |

### `field()` — cas spéciaux

```python
@dataclass
class Task:
    titre: str
    tags: list[str] = field(default_factory=list)      # ✅ jamais []  comme défaut
    created_at: datetime = field(default_factory=datetime.now)
    secret: str = field(repr=False)                    # exclu de __repr__
    _cache: dict = field(default_factory=dict, compare=False)  # pas pris en compte dans __eq__
```

### Dataclass `frozen` = hashable

```python
@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int


positions = {Coord(0, 0): "départ", Coord(5, 3): "arrivée"}   # ✅ clés OK
```

Frozen + slots + kw_only est un excellent **défaut** pour les "value objects".

### Quand NE PAS utiliser une dataclass

- Héritage complexe, comportement riche → classe normale.
- Modèle avec validation et serialization → **Pydantic** (Ch. 15).
- Juste un paquet de constantes → `Enum` ou module.

## 5. Validation et propriétés (`@property`)

Problème : les dataclasses n'ont pas de validation intégrée.

```python
@dataclass
class Personne:
    age: int     # rien n'empêche age = -5

p = Personne(-5)   # accepté, mais absurde
```

### Solution A : `__post_init__`

```python
@dataclass
class Personne:
    nom: str
    age: int

    def __post_init__(self):
        if self.age < 0:
            raise ValueError(f"âge invalide: {self.age}")
```

### Solution B : `@property` avec setter

Pour une **validation continue** (pas juste à la création) :

```python
class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius     # appelle le setter

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("zéro absolu dépassé")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:       # propriété dérivée, lecture seule
        return self._celsius * 9 / 5 + 32


t = Temperature(20)
t.celsius                # 20.0
t.fahrenheit             # 68.0
t.celsius = -300         # ValueError
```

`@property` transforme une méthode en "attribut calculé". Trois rôles :

1. **Lecture seule** : expose une valeur dérivée (`fahrenheit`).
2. **Validation** : contrôle à chaque assignation.
3. **Compatibilité ascendante** : convertir un attribut existant en propriété sans casser l'API.

**N'abusez pas** : si un attribut n'a besoin d'aucune validation, laissez-le public. Python n'aime pas les getters/setters pour rien.

## 6. Encapsulation "à la Python"

Python n'a pas de vrais modificateurs `private`/`protected`. Convention :

- `nom` : public.
- `_nom` : "privé" (convention : n'utilisez pas depuis l'extérieur).
- `__nom` : **name mangling** (renommé en `_Classe__nom` par l'interpréteur, évite les collisions en héritage).

```python
class Compte:
    def __init__(self, solde):
        self._solde = solde           # convention "privé"
        self.__hash_interne = 42      # mangled → _Compte__hash_interne
```

`__nom` n'est **pas** pour la sécurité (trivialement accessible). C'est pour éviter les collisions d'attributs en héritage multiple. À utiliser rarement.

## 7. Classes vs dictionnaires

Question fréquente : "pourquoi une classe au lieu d'un dict ?"

- **Classe** : structure **figée** de champs, méthodes associées, typage, documentation.
- **Dict** : structure **dynamique** de paires clé/valeur, pas de contrat.

Règle : si l'ensemble des champs est connu et fixe, c'est une classe (dataclass typiquement). Si les clés sont du contenu dynamique (config utilisateur, réponse API variable), c'est un dict.

---

### Piège courant : muter un attribut de classe

```python
class Counter:
    count = 0

    def incr(self):
        Counter.count += 1    # mute la variable de classe → partagée


a = Counter(); b = Counter()
a.incr(); a.incr(); b.incr()
print(a.count, b.count)       # 3 3 (peut surprendre)
```

Si vous voulez une variable partagée : c'est un attribut de classe. Si vous voulez un compteur par instance : attribut d'instance initialisé dans `__init__`.

---

### Sous le capot : résolution d'attribut

Quand vous faites `obj.attr`, Python cherche dans l'ordre :

1. L'instance (`obj.__dict__`)
2. La classe (`type(obj).__dict__`)
3. Les classes parentes (MRO, voir Ch. 8)
4. Descripteurs (Ch. 11)

Si rien n'est trouvé : `AttributeError`. (Sauf si `__getattr__` est défini — Ch. 13.)

`attr` en assignation (`obj.attr = v`) crée **toujours** un attribut d'instance (ne touche pas à la classe). C'est ce qui explique le piège de la mutation de classe.

---

## À retenir

- Attribut de classe = partagé. Ne jamais y mettre une valeur mutable.
- `@classmethod` pour les factories alternatives, `@staticmethod` pour les fonctions liées logiquement.
- Implémentez toujours `__repr__`. `__str__` est facultatif.
- Si `__eq__` custom, alors `__hash__` aussi (ou `= None`).
- Dataclasses par défaut : `@dataclass(frozen=True, slots=True, kw_only=True)` pour les value objects.
- `@property` pour la validation et les attributs calculés, pas pour tout.
- `_nom` convention, `__nom` name mangling (rare).

---

➡️ [Chapitre 8 — POO avancée](../08_poo_avancee/README.md)
