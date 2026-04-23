# Chapitre 1 — Écosystème Python moderne

Avant d'écrire une ligne de code, un développeur Python doit maîtriser son outillage. Un mauvais setup est la source n°1 des "ça marche chez moi" et des heures perdues. Ce chapitre n'est pas optionnel.

## 1. Choisir sa version de Python

CPython sort une version majeure par an (octobre). Chaque version est supportée ~5 ans. En 2026, les versions **supportées** sont 3.11, 3.12, 3.13, 3.14.

Règle : **ne jamais utiliser le Python du système** (`/usr/bin/python3` sur macOS/Linux). Il appartient à l'OS, le modifier casse des outils système.

### Vérifier ce qui est installé

```bash
python --version       # peut pointer vers n'importe quoi
python3 --version
which python3
```

### Installer proprement plusieurs versions

Deux options modernes :

**Option A — `uv` (recommandée, 2024+)**

[`uv`](https://docs.astral.sh/uv/) est un gestionnaire écrit en Rust par Astral (les auteurs de `ruff`). Il remplace `pip`, `virtualenv`, `pyenv` et `pip-tools` en un seul binaire, ~10 à 100× plus rapide.

```bash
# Installation (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Installer Python 3.12
uv python install 3.12
uv python list
```

**Option B — `pyenv` (historique)**

```bash
# macOS
brew install pyenv

pyenv install 3.12.7
pyenv global 3.12.7
```

Pour ce tutoriel on utilisera `uv`, mais les commandes sont traduisibles en `pip`/`venv` classiques.

## 2. Les environnements virtuels : pourquoi, toujours

Un projet Python a des **dépendances spécifiques** (ex : FastAPI 0.110, Pydantic 2.5). Installer ces paquets globalement est une erreur : le projet suivant en voudra d'autres versions, ça casse.

Un **environnement virtuel** (`venv`) est un dossier isolé contenant :
- un interpréteur Python
- ses propres paquets dans `lib/python3.X/site-packages/`

Aucun paquet global n'est "vu" depuis l'intérieur d'un venv activé.

### Créer et activer

```bash
# Avec uv
uv venv --python 3.12
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows PowerShell

# Vérifier
which python                   # -> .../projet/.venv/bin/python
python --version               # -> Python 3.12.x
```

Activer = modifier `PATH` pour que `python` pointe vers `.venv/bin/python`. Désactiver :

```bash
deactivate
```

### Installer des paquets

```bash
uv pip install requests         # uv : rapide
# ou : pip install requests     # classique
```

### Figer les dépendances

```bash
uv pip freeze > requirements.txt
```

> **Piège courant** — Ne jamais commit le dossier `.venv/` (il est lié à votre machine). Ajoutez-le à `.gitignore`.

## 3. Structure d'un projet moderne

Un projet Python professionnel ressemble à :

```
mon-projet/
├── .gitignore
├── .python-version           # version Python épinglée (uv/pyenv)
├── pyproject.toml            # métadonnées + dépendances (PEP 621)
├── README.md
├── src/
│   └── mon_projet/           # le paquet (underscore, pas tiret)
│       ├── __init__.py
│       └── core.py
└── tests/
    └── test_core.py
```

Deux choix structurels à comprendre :

### `src-layout` vs `flat-layout`

- **flat-layout** : le code est à la racine (`mon_projet/` à côté de `tests/`).
- **src-layout** : le code est dans `src/mon_projet/`.

Le `src-layout` est **recommandé** : il force à installer le paquet (`uv pip install -e .`) avant de pouvoir l'importer. Cela garantit que vous testez la version **installée** et non un bricolage de `PYTHONPATH`.

### `pyproject.toml` — le seul fichier de config dont vous avez besoin

```toml
[project]
name = "mon-projet"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.31",
    "pydantic>=2.5",
]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

`pyproject.toml` remplace `setup.py`, `setup.cfg`, `requirements.txt` (PEP 518, 621). Tous les outils modernes (ruff, mypy, pytest) lisent leur config dedans.

## 4. L'interpréteur interactif (REPL)

Python est un langage **interprété** : on peut exécuter du code ligne par ligne.

```bash
python
>>> 2 + 2
4
>>> import this
```

### `ipython` — un REPL décent

Le REPL de base est pauvre (pas d'historique persistant, pas d'auto-complétion riche, pas de coloration). Installez `ipython` :

```bash
uv pip install ipython
ipython
```

Fonctionnalités clés :
- `?obj` : aide sur un objet
- `??obj` : affiche le code source
- `%timeit expr` : chronomètre
- `%run script.py` : exécute un script dans la session

## 5. Exécuter du code

Trois façons :

```bash
python script.py                 # exécute un fichier
python -m mon_module             # exécute un module (préféré pour paquets)
python -c "print('hello')"       # exécute une expression
```

Le flag `-m` est important. Il lance le module comme un script, avec un `PYTHONPATH` correct. Exemple réel : `python -m http.server 8000` lance un serveur HTTP.

## 6. Choisir son IDE

Deux options réalistes en 2026 :

| IDE | Avantages | Inconvénients |
|---|---|---|
| **PyCharm** (Pro) | Refactoring avancé, debugger intégré, support Django/FastAPI riche | Payant, lourd |
| **VS Code + extension Python + Pylance** | Gratuit, léger, écosystème d'extensions | Config initiale plus manuelle |

Les deux supportent : type checking temps réel, debugger visuel, intégration git, environnement virtuel auto-détecté.

## 7. Vérifier votre installation

```bash
# Tout ce qui suit doit fonctionner :
python --version                          # 3.12+
python -c "import sys; print(sys.path)"   # liste contient votre .venv
uv --version                              # si vous utilisez uv
```

---

### Piège courant : le "wrong Python"

Vous venez d'installer un paquet avec `pip install X`, puis `import X` échoue. Cause : `pip` et `python` pointent vers **des interpréteurs différents**. Toujours vérifier :

```bash
which python
which pip
python -m pip install X    # garantit la cohérence : on utilise le pip DE python
```

La règle d'or : utiliser `python -m pip ...` plutôt que `pip ...` directement.

---

### Sous le capot : qu'est-ce qu'un `.venv` ?

Ce n'est **pas** une copie de Python. C'est un dossier contenant :
- Un fichier `pyvenv.cfg` qui pointe vers l'interpréteur "parent"
- Des liens symboliques vers le `python` parent (`bin/python` → `/usr/local/bin/python3.12`)
- Un dossier `site-packages` **vide** au départ
- Des scripts d'activation

Activer le venv modifie `sys.path` pour que Python cherche ses modules dans le `site-packages` local **avant** celui du système.

---

## À retenir

- Une version de Python par projet, jamais le Python système.
- Un `.venv` par projet, **toujours**.
- `pyproject.toml` est la source de vérité pour dépendances et config.
- `python -m pip` > `pip`.
- `src-layout` évite 90% des soucis d'import.

---

➡️ [Chapitre 2 — Modèle objet & types primitifs](../02_fondations/README.md)
