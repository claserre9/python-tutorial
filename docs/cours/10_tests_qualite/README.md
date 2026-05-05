# Chapitre 10 — Typage statique & qualité de code

Typer son code statiquement et le vérifier avec **mypy** ou **pyright**. Tester avec **pytest**. Lint et format avec **ruff**. Chapitre qui transforme un script jetable en code **maintenable**. Se termine par le **projet fil rouge du Niveau 2** : un parseur de logs entièrement typé et testé.

## 1. Type hints — au-delà des bases

Rappel (Ch. 4) : les annotations sont **indicatives**. Elles ne s'exécutent pas. Elles sont lues par les IDE et les type checkers.

### Collections et unions

```python
# 3.9+
scores: list[int] = []
config: dict[str, int] = {}

# 3.10+
def find(id: int) -> User | None: ...
def parse(s: str | bytes) -> int: ...
```

### `Optional`, `Literal`, `Any`, `Never`

```python
from typing import Optional, Literal, Any, Never

# Optional[X] = X | None (équivalent, 3.10+ préfère |)
def find(id: int) -> Optional[User]: ...

# Literal : valeurs précises
Couleur = Literal["rouge", "vert", "bleu"]
def colorier(c: Couleur) -> None: ...
colorier("violet")           # mypy : ERROR

# Any : désactive le type check
def legacy(x: Any) -> Any: ...

# Never : fonctions qui ne retournent jamais (exception, boucle infinie)
def erreur_fatale(msg: str) -> Never:
    raise RuntimeError(msg)
```

### Generics : `TypeVar`

Pour créer des conteneurs / fonctions génériques :

```python
from typing import TypeVar

T = TypeVar("T")

def premier(items: list[T]) -> T:
    return items[0]


# mypy infère :
premier([1, 2, 3])         # int
premier(["a", "b"])        # str
```

### Syntaxe générique 3.12+ (PEP 695)

Depuis Python 3.12, pas besoin de `TypeVar` explicite :

```python
def premier[T](items: list[T]) -> T:
    return items[0]


class Stack[T]:
    def __init__(self):
        self._items: list[T] = []

    def push(self, x: T) -> None:
        self._items.append(x)

    def pop(self) -> T:
        return self._items.pop()
```

Plus propre, plus lisible. Utilisez cette syntaxe si vous êtes en 3.12+.

### `TypedDict` — dicts typés

```python
from typing import TypedDict

class UserDict(TypedDict):
    id: int
    nom: str
    email: str | None


def creer(user: UserDict) -> None:
    print(user["nom"])


creer({"id": 1, "nom": "Alice", "email": None})      # OK
creer({"id": 1, "nom": "Alice"})                      # ERROR : email manquant
```

Pour du JSON entrant / sortant. Alternative légère à Pydantic.

### `NewType` — marquage distinctif

```python
from typing import NewType

UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)


def acheter(user: UserId, order: OrderId) -> None: ...


u = UserId(1)
o = OrderId(2)

acheter(u, o)       # OK
acheter(o, u)       # mypy : ERROR — même si ce sont des int à l'exécution
```

Empêche de mélanger deux `int` sémantiquement différents.

### `Self` (3.11+)

```python
from typing import Self

class Builder:
    def with_name(self, n: str) -> Self:
        self.name = n
        return self
```

`Self` fait que la méthode retourne exactement le type de la classe courante (préserve la sous-classe).

### `Callable`, `Awaitable`

```python
from collections.abc import Callable, Awaitable

handler: Callable[[int, str], bool]
async_fn: Callable[[int], Awaitable[str]]
```

### `ParamSpec` — wrapper qui préserve la signature (décorateurs)

```python
from typing import ParamSpec, TypeVar, Callable
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")

def log_appel(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"{fn.__name__} called")
        return fn(*args, **kwargs)
    return wrapper
```

Essentiel quand on type des décorateurs génériques (Ch. 11).

## 2. mypy / pyright

### Installation et config

```bash
uv pip install mypy
```

Config dans `pyproject.toml` :

```toml
[tool.mypy]
python_version = "3.12"
strict = true
disallow_untyped_defs = true
warn_unused_ignores = true
```

`strict = true` active toutes les vérifications sévères. Plus dur au début, beaucoup de bugs attrapés.

### Exécution

```bash
mypy src/
```

### Ignorer ponctuellement

```python
result = legacy_function()     # type: ignore[no-any-return]
```

Toujours spécifier le code d'erreur ignoré. Un `# type: ignore` nu est une odeur de code.

### pyright vs mypy

- **mypy** : référence, plus strict par défaut, un peu lent sur gros projets.
- **pyright** (Microsoft) : plus rapide, plus permissif par défaut, embarqué dans VS Code Pylance.

Utilisez celui qui vous convient. Les deux lisent vos annotations.

## 3. pytest — tests unitaires

### Structure

```
projet/
├── src/
│   └── mon_projet/
│       └── calcul.py
└── tests/
    └── test_calcul.py
```

### Écrire un test

```python
# tests/test_calcul.py
from mon_projet.calcul import additionner

def test_additionner_positifs():
    assert additionner(2, 3) == 5

def test_additionner_negatifs():
    assert additionner(-1, -2) == -3
```

Lancer : `pytest` (auto-découverte des fichiers `test_*.py`).

### `assert` et introspection

`pytest` réécrit les `assert` pour afficher des diagnostics riches :

```python
def test_listes():
    assert [1, 2, 3] == [1, 2, 4]
```

Sortie :
```
assert [1, 2, 3] == [1, 2, 4]
  At index 2 diff: 3 != 4
```

Pas besoin de `self.assertEquals(...)` à la Java.

### Tester les exceptions

```python
import pytest

def test_division_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_message():
    with pytest.raises(ValueError, match="invalide"):
        int("abc")
```

### `parametrize` — données multiples

```python
@pytest.mark.parametrize("a, b, attendu", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_additionner(a, b, attendu):
    assert additionner(a, b) == attendu
```

Affiche 3 tests distincts. Permet de couvrir beaucoup de cas sans duplication.

### Fixtures

Une fixture = donnée/ressource préparée pour un test.

```python
@pytest.fixture
def user():
    return {"id": 1, "nom": "Alice"}

def test_nom(user):           # pytest injecte la fixture
    assert user["nom"] == "Alice"
```

Avec teardown :

```python
@pytest.fixture
def db(tmp_path):
    conn = sqlite3.connect(tmp_path / "test.db")
    yield conn                # la partie avant yield est le setup
    conn.close()              # la partie après yield est le teardown
```

Fixtures built-in utiles :
- `tmp_path` : `Path` vers un dossier temporaire unique.
- `monkeypatch` : modifier/restaurer des attributs ou variables d'env.
- `capsys` : capturer `stdout`/`stderr`.

### `conftest.py`

Placer des fixtures partagées entre fichiers dans `tests/conftest.py`. Auto-découvert par pytest.

### Mocking

```python
from unittest.mock import Mock, patch

def test_envoi(monkeypatch):
    send = Mock(return_value=True)
    monkeypatch.setattr("mon_module.smtp_send", send)

    action()
    send.assert_called_once_with("a@b.com", "hello")
```

### Couverture

```bash
uv pip install pytest-cov
pytest --cov=src --cov-report=term-missing
```

Objectif raisonnable : 80-90%. Pas 100% (la quête du 100% fait écrire des tests inutiles).

## 4. ruff — lint et format

`ruff` (Rust, ultra-rapide) remplace `flake8`, `isort`, `pylint` (partiellement) et `black`.

### Installation et config

```bash
uv pip install ruff
```

Dans `pyproject.toml` :

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "SIM", "RUF"]
ignore = []

[tool.ruff.format]
quote-style = "double"
```

Règles courantes :
- `E`, `W` : PEP 8 (erreurs + warnings)
- `F` : pyflakes (imports inutilisés, variables non définies)
- `I` : isort (tri des imports)
- `UP` : pyupgrade (suggère des syntaxes modernes)
- `B` : bugbear (pièges courants)
- `SIM` : simplification
- `RUF` : règles spécifiques à ruff

### Commandes

```bash
ruff check .               # lint
ruff check --fix .         # corrige ce qu'il peut
ruff format .              # format (comme black)
```

### pre-commit

Exécuter ruff et mypy automatiquement avant chaque commit :

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
```

Installation :

```bash
uv pip install pre-commit
pre-commit install
```

## 5. Docstrings et style PEP 8

### PEP 8 rappel

- 4 espaces d'indentation (jamais de tabs).
- Lignes ≤ 79 caractères (relâché à 100-120 dans la pratique moderne).
- `snake_case` pour fonctions/variables, `PascalCase` pour classes, `SCREAMING_SNAKE` pour constantes.
- Deux lignes vides entre fonctions/classes top-level, une entre méthodes.
- Imports groupés (stdlib / tiers / locaux), triés.

Ruff fait appliquer tout ça.

### Docstrings — styles

**Google** :

```python
def diviser(a: float, b: float) -> float:
    """Divise a par b.

    Args:
        a: le dividende.
        b: le diviseur (non nul).

    Returns:
        Le résultat.

    Raises:
        ValueError: si b = 0.
    """
```

Choisissez un style, tenez-vous-y. `mkdocstrings` et Sphinx savent les parser.

---

## 6. Projet fil rouge — Parseur de logs

### Cahier des charges

Une lib `logparser` qui :

1. Lit un fichier de logs au format Nginx **combined** (une ligne = un accès).
2. Parse chaque ligne en `LogEntry` (dataclass typée).
3. Expose des fonctions d'analyse : top IPs, compte par code de status, volume par heure.
4. Gère proprement les lignes mal formées (ignore + warn, ou exception selon le contexte).

### Contraintes

- **100% typé** (mypy strict passe).
- **Tests** : ≥ 80% couverture, fixtures pour les logs d'exemple.
- **Lint** : ruff + mypy clean.
- Lib importable + CLI d'exemple (`python -m logparser access.log --top 10`).
- Pipeline interne construit avec des **générateurs** (Ch. 9).

### Structure

```
logparser/
├── pyproject.toml
├── src/logparser/
│   ├── __init__.py
│   ├── models.py       # LogEntry (dataclass)
│   ├── parser.py       # ligne → LogEntry ; gestion parsing
│   ├── analytics.py    # top IPs, status counts, etc.
│   └── __main__.py     # CLI
└── tests/
    ├── conftest.py
    ├── test_parser.py
    └── test_analytics.py
```

Squelette et solution complète dans `exercices/10_tests_qualite/logparser/` et `solutions/10_tests_qualite/logparser/`.

---

### Piège courant : annotations "stringifiées" et références forward

```python
class Node:
    def add_child(self, child: Node) -> None:     # ❌ Node n'existe pas encore ici
        ...
```

Fix 1 : `from __future__ import annotations` — toutes les annotations deviennent des strings, évaluées à la demande.

Fix 2 : guillemets `child: "Node"`.

Fix 3 (3.11+) : utiliser `Self` :

```python
from typing import Self
def add_child(self, child: Self) -> None: ...
```

---

### Sous le capot : annotations à l'exécution

Les annotations sont stockées dans `__annotations__` :

```python
def f(x: int, y: str) -> bool: ...
f.__annotations__
# {'x': int, 'y': str, 'return': bool}
```

Pour les obtenir de manière robuste (avec forward refs résolues) :

```python
from typing import get_type_hints
get_type_hints(f)
```

Pydantic, dataclasses, FastAPI s'appuient tous sur ce mécanisme (Ch. 13).

---

## À retenir

- Typez tout nouveau code. Activez `strict` dans mypy.
- Préférez `X | None`, `list[int]`, syntaxe `[T]` 3.12+.
- `Protocol` pour les interfaces, `TypedDict` pour les dicts de données, `NewType` pour éviter les confusions.
- pytest : `assert` + `parametrize` + fixtures + `tmp_path` couvrent 90% des cas.
- ruff : lint + format en un outil.
- pre-commit enchaîne ruff + mypy avant chaque commit.
- Couverture ~85%, pas 100%.

---

➡️ [Chapitre 11 — Décorateurs & descripteurs](../11_decorateurs/README.md)
