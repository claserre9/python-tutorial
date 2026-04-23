# Solutions — Chapitre 1

## 1.1 — Diagnostic

Il n'y a pas de "bonne" réponse unique, mais voici ce que vous devriez observer.

- `python --version` peut ne pas exister (surtout macOS/Linux récents). `python3 --version` devrait marcher.
- `which python3` pointe typiquement vers `/usr/bin/python3` (système) ou `/opt/homebrew/bin/python3` (Homebrew).
- `sys.executable` donne le **chemin absolu** de l'interpréteur utilisé — c'est la source de vérité.

**Point clé** : `python --version` vous ment potentiellement. `sys.executable` jamais.

## 1.2 — Environnement virtuel

```bash
mkdir playground && cd playground
uv venv --python 3.12
source .venv/bin/activate
which python    # .../playground/.venv/bin/python   ← dans le venv
uv pip install requests
deactivate
python -c "import requests"   # ModuleNotFoundError (si pas d'install globale)
```

Ce qu'il faut retenir : `activate` ne fait que modifier `PATH`. Rien de magique.

## 1.3 — `pyproject.toml`

```toml
[project]
name = "playground"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.31",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.5",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Structure minimale pour que `pip install -e .` fonctionne :

```
playground/
├── pyproject.toml
└── src/
    └── playground/
        └── __init__.py
```

Le `src-layout` exige que votre paquet soit dans `src/playground/`. Sinon, ajoutez dans `pyproject.toml` :

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/playground"]
```

## 1.4 — `python -m` vs script

- `python hello.py` : exécute le **fichier**. Le `sys.path[0]` est le dossier contenant `hello.py`.
- `python -m hello` : exécute le **module** `hello`. Nécessite que `hello.py` soit importable (présent dans `sys.path`). Le `sys.path[0]` est le répertoire courant.

Pour un paquet (avec `__init__.py`), seul `python -m mon_paquet` fonctionne correctement. C'est pour ça qu'on écrit souvent `python -m pytest` plutôt que `pytest` — ça garantit que pytest utilise le Python du venv actif.

`python -m http.server 8000` lance un serveur HTTP basique qui liste le contenu du dossier courant. Pratique pour tester des fichiers statiques.

## 1.5 — Le bug "wrong Python"

Le bug se produit quand :
- `pip` vient d'une installation Python A (ex. `/usr/bin/pip`, Python 3.9 du système)
- `python` vient d'une installation Python B (ex. `/opt/homebrew/bin/python3`, Python 3.12)

Alors `pip install X` place `X` dans le `site-packages` de A, mais `python` cherche dans B.

**Solution universelle** :

```bash
python -m pip install X
```

Ici on invoque explicitement le `pip` associé à `python`. Même logique pour `pytest`, `ruff`, etc. : préférez `python -m pytest` à `pytest`.

---

## Pour aller plus loin

- Lisez [PEP 518](https://peps.python.org/pep-0518/) et [PEP 621](https://peps.python.org/pep-0621/) — les fondations de `pyproject.toml`.
- Parcourez le [guide officiel de packaging](https://packaging.python.org/en/latest/).
- Si vous utilisez `uv`, lisez la section ["Working on projects"](https://docs.astral.sh/uv/guides/projects/) de sa doc.
