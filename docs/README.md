# Tutoriel Python — Du débutant à l'expert

Parcours progressif en **3 niveaux** pour passer de la syntaxe de base à la maîtrise réelle de CPython, la concurrence, la métaprogrammation et le packaging moderne.

Cible : Python **3.12+**. Les exemples utilisent `uv` pour la gestion d'environnement.

## Structure

- `cours/` — théorie commentée avec exemples exécutables
- `exercices/` — énoncés à compléter
- `solutions/` — corrigés commentés

Chaque niveau se termine par un **projet fil rouge** qui consolide les chapitres précédents.

## Sommaire

### Niveau 1 — Fondamentaux
*Projet fil rouge : CLI de gestion de tâches (JSON, argparse, logging)*

1. Écosystème Python moderne
2. Modèle objet & types primitifs
3. Flux de contrôle (incl. pattern matching structurel)
4. Fonctions & scope (LEGB, closures, type hints)
5. Structures de données (+ complexité algorithmique)
6. I/O, exceptions, logging — **+ projet CLI todo**

### Niveau 2 — Intermédiaire
*Projet fil rouge : parseur de logs typé, testé, packagé*

7. POO : bases solides (dataclasses, dunders)
8. POO avancée (MRO, `super()` coopératif, Protocol vs ABC, `__slots__`)
9. Itérateurs, générateurs, fonctionnel (`itertools`, `functools`)
10. Typage statique & qualité (mypy, pytest, ruff) — **+ projet parseur de logs**

### Niveau 3 — Expert
*Projet fil rouge : API FastAPI async + worker, publiée sur PyPI*

11. Décorateurs & descripteurs
12. Concurrence & async (GIL, threading, multiprocessing, asyncio, TaskGroup)
13. Métaprogrammation & introspection (métaclasses, `__init_subclass__`, `inspect`)
14. Performance & internals CPython (profilage, `__slots__`, `weakref`, gc)
15. Dev web moderne avec FastAPI (Pydantic v2, SQLAlchemy async)
16. Packaging & distribution — **+ projet API publiée**

### Annexes
- **[A. Debug](annexes/A_debug.md)** — `pdb`, `ipdb`, debuggers IDE, post-mortem
- **[B. Regex](annexes/B_regex.md)** — `re`, groupes nommés, pièges (ReDoS)
- **[C. Bases de données](annexes/C_bases_donnees.md)** — `sqlite3`, SQLAlchemy 2.0, Alembic
- **[D. Sécurité](annexes/D_securite.md)** — secrets, injections, audit de dépendances

## Prérequis

- Python 3.12 ou plus récent
- [`uv`](https://docs.astral.sh/uv/) recommandé (alternative : `pip` + `venv`)
- Un IDE avec support Python (PyCharm, VS Code)

## Installation

```bash
# Avec uv (recommandé)
uv venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
uv pip install -r requirements.txt

# Ou avec pip classique
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Comment étudier

1. Lire `cours/NN_.../README.md`
2. Faire les exercices dans `exercices/NN_.../`
3. Comparer avec `solutions/NN_.../` **après** avoir tenté
4. Ne pas sauter les encadrés "Piège courant" et "Sous le capot"

Commencez par [Chapitre 1 — Écosystème Python moderne](cours/01_intro_installation/README.md).
