# Chapitre 16 — Packaging & distribution

Transformer votre code en **paquet installable** — localement, pour vos collègues, ou sur PyPI. `pyproject.toml` moderne, choix entre `uv` / `hatch` / `poetry`, publication, versioning, documentation, CI. Chapitre final qui clôt le parcours avec le **projet fil rouge du Niveau 3** : une API FastAPI async publiée.

## 1. Anatomie d'un projet distribuable

```
mon-paquet/
├── .github/workflows/ci.yml     # CI
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
├── CHANGELOG.md
├── pyproject.toml               # la source de vérité
├── src/
│   └── mon_paquet/              # nom importable (underscore)
│       ├── __init__.py
│       ├── py.typed             # marqueur "ce paquet est typé" (PEP 561)
│       └── core.py
└── tests/
    └── test_core.py
```

**Convention importante** : le **nom du projet** (dans `pyproject.toml`) peut être `mon-paquet` (avec tiret), mais le **nom du paquet Python** est `mon_paquet` (avec underscore). Les tirets ne sont pas valides dans `import`.

## 2. `pyproject.toml` — référence PEP 621

```toml
[project]
name = "mon-paquet"
version = "0.1.0"
description = "Description courte."
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.12"
authors = [
    { name = "Clifford", email = "claserre9@gmail.com" }
]
keywords = ["cli", "automation"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

dependencies = [
    "pydantic>=2.5",
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "mypy>=1.10", "ruff>=0.5"]
docs = ["mkdocs>=1.6", "mkdocs-material>=9.5"]

[project.urls]
Homepage = "https://github.com/user/mon-paquet"
Issues = "https://github.com/user/mon-paquet/issues"

[project.scripts]
mon-cli = "mon_paquet.cli:main"           # expose une commande shell

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/mon_paquet"]
```

### Points notables

- **`dependencies`** : versions minimales recommandées (`>=`). Évitez les `==` sauf raison précise.
- **`optional-dependencies`** : groupes extras installables via `pip install mon-paquet[dev]`.
- **`[project.scripts]`** : déclare des commandes shell. `pip install` crée un exécutable `mon-cli` pointant vers `main()`.
- **`py.typed`** : un fichier **vide** dans le paquet indique qu'il expose ses types aux consommateurs (PEP 561). Important si d'autres codes utilisent mypy avec votre paquet.

## 3. Build backend : qui choisir ?

Plusieurs outils implémentent le "build backend" (ce qui génère le `.whl` depuis le code).

| Tool | Usage principal | Avantages |
|---|---|---|
| **hatch** / hatchling | Build + gestion d'envs | Simple, rapide, recommandé par PyPA |
| **setuptools** | L'historique | Le plus répandu, toujours valable |
| **poetry** | All-in-one | Très populaire, écosystème mature ; format non-standard (a évolué vers PEP 621) |
| **flit** | Simple, pour petits paquets | Minimal |
| **uv** | Tout-en-un ultra-rapide | Remplace pip + venv + build ; utilise hatchling en dessous |

En 2026, recommandation : **`uv` + `hatchling`** pour la plupart des projets. Simple, rapide, standardisé.

## 4. `uv` — commandes essentielles

```bash
uv init mon-paquet                # crée un squelette
cd mon-paquet

uv venv                            # crée .venv
uv add requests                    # ajoute une dép (et met à jour pyproject.toml)
uv add --dev pytest               # ajoute en dev
uv remove requests
uv sync                            # installe exactement les deps
uv lock                            # régénère uv.lock

uv run pytest                      # exécute dans le venv sans l'activer
uv build                           # construit dist/*.whl et *.tar.gz
uv publish                         # publie sur PyPI (nécessite credentials)
```

Le fichier **`uv.lock`** fige les versions exactes de toutes les deps transitives (reproductibilité).

## 5. `src-layout` vs `flat-layout`

Déjà vu au Ch. 1. Rappel :

- `src-layout` (dans `src/mon_paquet/`) : force le test **sur le paquet installé**, pas sur un bricolage de `PYTHONPATH`. **Recommandé**.
- `flat-layout` (`mon_paquet/` à la racine) : plus simple pour tout petit projet.

## 6. Versioning sémantique

Format `MAJOR.MINOR.PATCH` :
- **MAJOR** : breaking change d'API.
- **MINOR** : ajout rétrocompatible.
- **PATCH** : fix rétrocompatible.

Exemples : `0.x.x` pour "pas encore stable", `1.0.0` pour première API stable.

### Outils automatiques

- **`bumpversion`** / **`hatch version`** : bump en ligne de commande.
- **`python-semantic-release`** : détermine la version depuis les commits (style Conventional Commits).

## 7. Publier sur PyPI

### Créer un compte

1. S'inscrire sur [pypi.org](https://pypi.org/) (et **test.pypi.org** pour les tests).
2. Activer **2FA**.
3. Créer un **API token** dans les paramètres.

### Publier

```bash
# Construire
uv build

# Publier (nécessite un token dans ~/.pypirc ou variable d'env UV_PUBLISH_TOKEN)
uv publish

# Ou avec twine (historique)
uv pip install twine
twine upload dist/*
```

### Tester d'abord sur TestPyPI

```bash
uv publish --publish-url https://test.pypi.org/legacy/
pip install --index-url https://test.pypi.org/simple/ mon-paquet
```

Ça évite de polluer PyPI si votre setup a un bug.

## 8. Documentation avec MkDocs Material

```bash
uv add --dev mkdocs-material mkdocstrings[python]
mkdocs new .
```

`mkdocs.yml` :

```yaml
site_name: Mon Paquet
theme:
  name: material
  features:
    - navigation.tabs
    - content.code.copy

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            docstring_style: google

nav:
  - Accueil: index.md
  - Guide: guide.md
  - Référence: reference.md
```

```bash
mkdocs serve      # preview locale sur :8000
mkdocs build      # génère site/ statique
```

### Publication GitHub Pages

```bash
mkdocs gh-deploy
```

## 9. CI avec GitHub Actions

`.github/workflows/ci.yml` :

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up uv
        uses: astral-sh/setup-uv@v3
        with:
          enable-cache: true

      - name: Install Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install deps
        run: uv sync --all-extras

      - name: Lint
        run: uv run ruff check .

      - name: Type check
        run: uv run mypy src/

      - name: Test
        run: uv run pytest --cov=src
```

Pour **publier automatiquement** sur une nouvelle tag `vX.Y.Z` :

```yaml
release:
  needs: test
  if: startsWith(github.ref, 'refs/tags/v')
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v3
    - run: uv build
    - run: uv publish
      env:
        UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

## 10. Changelog et releases

Maintenir un `CHANGELOG.md` style [Keep a Changelog](https://keepachangelog.com/) :

```markdown
# Changelog

## [0.2.0] - 2026-05-15
### Added
- Support de l'export CSV.
### Fixed
- Plantage sur les fichiers vides.

## [0.1.0] - 2026-04-20
### Added
- Première version publique.
```

Sur GitHub, créer une **Release** associée à la tag. Vos utilisateurs sont notifiés.

## 11. Bonnes pratiques supplémentaires

- **`.gitignore`** adapté à Python (`__pycache__/`, `.venv/`, `dist/`, `.pytest_cache/`, `.mypy_cache/`, `htmlcov/`).
- **`.pre-commit-config.yaml`** qui lance ruff + mypy + tests rapides avant chaque commit.
- **Badges** dans le README (CI, coverage, PyPI version).
- **`LICENSE`** : MIT, Apache-2.0, ou BSD-3 pour du code open-source permissif.

---

## 12. Projet fil rouge Niveau 3 — API FastAPI packagée

### Cahier des charges

Une API `api_taches` qui :

1. Gère des tâches (créer, lister, marquer done, supprimer) — comme le projet Niv. 1 mais en API.
2. Utilise **FastAPI async** + **SQLAlchemy 2.0 async** + SQLite (facilement upgradable vers Postgres).
3. Authentification JWT (login via `/token`).
4. **100% typé**, tests `httpx.AsyncClient`, mypy strict, ruff clean, couverture ≥ 80%.
5. **Packagé** avec `pyproject.toml`, CI GitHub Actions, docs MkDocs.
6. Expose une CLI `api-taches serve` qui lance uvicorn.

### Structure

```
api_taches/
├── .github/workflows/ci.yml
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
├── mkdocs.yml
├── src/api_taches/
│   ├── __init__.py
│   ├── py.typed
│   ├── app.py              # app FastAPI
│   ├── cli.py              # entrée console
│   ├── config.py           # settings via Pydantic
│   ├── db.py               # SQLAlchemy async engine/session
│   ├── models.py           # ORM
│   ├── schemas.py          # Pydantic IN/OUT
│   ├── auth.py             # JWT, hash
│   └── routers/
│       ├── taches.py
│       └── auth.py
├── docs/
│   └── index.md
└── tests/
    ├── conftest.py
    ├── test_taches.py
    └── test_auth.py
```

Squelette et solution complète dans `exercices/16_packaging/api_taches/` et `solutions/16_packaging/api_taches/`.

Ce projet consolide **tout le Niveau 3** : async, typage, API, tests, packaging, CI, docs. C'est un modèle de projet Python moderne qu'on peut reproduire tel quel pour n'importe quel nouveau service.

---

### Piège courant : oublier `py.typed`

Sans `py.typed`, mypy des consommateurs ignore vos annotations. Toujours créer un fichier vide `src/mon_paquet/py.typed`.

---

### Sous le capot : wheels et sdists

Un paquet Python distribué existe sous deux formes :

- **Wheel** (`.whl`) : build pré-compilé, prêt à installer. Format binaire optimisé, architecture/platform si code C.
- **sdist** (`.tar.gz`) : source distribuée. `pip install` la compile à l'installation si nécessaire.

`uv build` génère les deux. PyPI accepte les deux. Pour une installation rapide, les utilisateurs téléchargent le wheel. Pour du pur Python, un seul wheel "universel" (`py3-none-any`) suffit.

---

## À retenir

- `pyproject.toml` (PEP 621) est **la** référence.
- `uv` + `hatchling` : recommandation 2026.
- `src-layout` et `py.typed` dans les paquets sérieux.
- Versioning sémantique + changelog.
- CI GitHub Actions pour tester sur plusieurs versions Python.
- Publication PyPI via `uv publish` (testée d'abord sur TestPyPI).
- Docs avec MkDocs Material + mkdocstrings.

---

Félicitations, vous êtes arrivé au bout du parcours. Les **annexes** ([A-D](../../annexes/)) approfondissent des sujets transversaux utiles : debug, regex, DB, sécurité.
