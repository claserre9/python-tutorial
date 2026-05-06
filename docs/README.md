# Tutoriel Python — Du débutant à l'expert

Parcours progressif en **3 niveaux** pour passer de la syntaxe de base à la maîtrise réelle de CPython, la concurrence, la métaprogrammation et le packaging moderne.

Cible : Python **3.12+**. Les exemples utilisent `uv` pour la gestion d'environnement.

## Structure du projet

```
python-tutorial/
├── docs/
│   ├── cours/          # Leçons théoriques avec exemples exécutables
│   ├── exercices/      # Exercices pratiques par chapitre
│   ├── solutions/      # Corrections annotées
│   └── annexes/        # Références et ressources complémentaires
```

## Sommaire

### Niveau 1 — Fondamentaux

| # | Chapitre | Thèmes abordés |
|---|----------|----------------|
| 1 | [Écosystème Python moderne](cours/01_intro_installation/README.md) | Installation, `uv`, `pip`, venv, REPL, Hello World |
| 2 | [Modèle objet & types primitifs](cours/02_fondations/README.md) | `int`, `float`, `str`, `bool`, `None`, mutabilité, références |
| 3 | [Flux de contrôle](cours/03_flux_controle/README.md) | `if/elif/else`, boucles, `match`, compréhensions |
| 4 | [Fonctions & scope](cours/04_fonctions_modules/README.md) | LEGB, closures, `*args`, `**kwargs`, type hints |
| 5 | [Structures de données](cours/05_structures_donnees/README.md) | `list`, `dict`, `set`, `tuple`, complexité algorithmique |
| 6 | [I/O, exceptions, logging](cours/06_fichiers_exceptions/README.md) | `open`, `pathlib`, `try/except`, `logging` — **Projet : CLI todo** |

### Niveau 2 — Intermédiaire

| # | Chapitre | Thèmes abordés |
|---|----------|----------------|
| 7 | [POO : bases solides](cours/07_poo_bases/README.md) | Classes, `dataclasses`, dunders, héritage |
| 8 | [POO avancée](cours/08_poo_avancee/README.md) | MRO, `super()` coopératif, Protocol vs ABC, `__slots__` |
| 9 | [Itérateurs, générateurs, fonctionnel](cours/09_concepts_experts/README.md) | `itertools`, `functools`, générateurs, `yield from` |
| 10 | [Typage statique & qualité](cours/10_tests_qualite/README.md) | `mypy`, `pytest`, `ruff` — **Projet : parseur de logs** |

### Niveau 3 — Expert

| # | Chapitre | Thèmes abordés |
|---|----------|----------------|
| 11 | [Décorateurs & descripteurs](cours/11_decorateurs/README.md) | `@wraps`, descripteurs, `__get__/__set__`, décorateurs paramétrés |
| 12 | [Concurrence & async](cours/12_concurrence/README.md) | GIL, `threading`, `multiprocessing`, `asyncio`, `TaskGroup` |
| 13 | [Métaprogrammation & introspection](cours/13_metaprogrammation/README.md) | Métaclasses, `__init_subclass__`, `inspect`, `ast` |
| 14 | [Performance & internals CPython](cours/14_performance/README.md) | `cProfile`, `memory_profiler`, `__slots__`, `weakref`, gc |
| 15 | [Dev web moderne avec FastAPI](cours/15_dev_web/README.md) | Pydantic v2, SQLAlchemy async, dépendances, auth |
| 16 | [Packaging & distribution](cours/16_packaging/README.md) | `pyproject.toml`, PyPI, CI/CD — **Projet : API publiée** |

## Prérequis

- Python 3.12 ou plus récent
- [`uv`](https://docs.astral.sh/uv/) recommandé (alternative : `pip` + `venv`)
- Un IDE avec support Python (PyCharm, VS Code)

## Installation rapide

```bash
git clone https://github.com/claserre9/python-tutorial.git
cd python-tutorial

# Avec uv (recommandé)
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Servir la documentation localement
mkdocs serve
```

La documentation est ensuite disponible sur `http://localhost:8000`.

## Parcours recommandé

1. Lire le cours du chapitre
2. Faire les exercices sans regarder les solutions
3. Comparer avec les solutions annotées
4. Ne pas sauter les encadrés "Piège courant" et "Sous le capot"

## Licence

MIT — Clifford
