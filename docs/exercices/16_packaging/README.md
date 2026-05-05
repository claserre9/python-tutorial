# Exercices — Chapitre 16 : Packaging

## Partie A — Exercice rapide sur `pyproject.toml`

Créez un `pyproject.toml` minimal pour un paquet `monbot` :

- Version 0.1.0
- Requiert Python 3.12+
- Dépend de `httpx >= 0.27` et `pydantic >= 2.5`
- Dev : `pytest`, `mypy`, `ruff`
- Expose la commande `monbot` pointant vers `monbot.cli:main`
- Utilise `hatchling` comme build backend
- `src-layout`

Fichier à créer : `monbot/pyproject.toml`. Testez avec :

```bash
cd monbot
uv pip install -e .
```

## Partie B — Projet fil rouge : API de tâches

Dossier `api_taches/`. Implémentez les étapes suivantes :

1. `pyproject.toml` complet (Pydantic + FastAPI + SQLAlchemy async + JWT)
2. Modèle DB : `User` et `Tache` (1-N, cascade delete)
3. Schémas Pydantic : `UserIn`, `UserOut`, `TacheIn`, `TacheOut`, `Token`
4. Auth JWT avec `passlib` pour les mots de passe
5. Routes :
   - `POST /register`, `POST /token`
   - `GET /taches`, `POST /taches`, `POST /taches/{id}/done`, `DELETE /taches/{id}`
6. Isolation par utilisateur (chaque user ne voit que ses tâches)
7. Tests `pytest-asyncio` avec DB SQLite temporaire par test
8. CI GitHub Actions (ruff + mypy + pytest)
9. CLI `api-taches serve`

### Contraintes

- `mypy --strict` doit passer
- Couverture tests ≥ 80%
- `ruff check` clean
- Doit s'installer via `uv pip install -e ".[dev]"` et exposer `api-taches`

### Tests requis

```
tests/
├── conftest.py          # fixture app + client httpx
├── test_auth.py         # register, login, route protégée
└── test_taches.py       # CRUD + isolation
```

Solution complète dans `solutions/16_packaging/api_taches/`.
