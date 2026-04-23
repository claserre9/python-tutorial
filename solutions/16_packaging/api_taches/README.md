# api-taches

API de gestion de tâches — projet fil rouge du Niveau 3.

Stack : **FastAPI** · **SQLAlchemy 2.0 async** · **SQLite** · **JWT** · **Pydantic v2**.

## Installation

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Utilisation

```bash
# Lancer le serveur
api-taches serve --reload

# Swagger UI : http://localhost:8000/docs
```

### Flux type

```bash
# Créer un compte
curl -X POST http://localhost:8000/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"me@ex.com","password":"longpass1"}'

# Récupérer un token
curl -X POST http://localhost:8000/token \
  -d 'username=me@ex.com&password=longpass1'
# -> {"access_token": "eyJ...", "token_type": "bearer"}

# Créer une tâche (avec le token)
curl -X POST http://localhost:8000/taches \
  -H 'Authorization: Bearer eyJ...' \
  -H 'Content-Type: application/json' \
  -d '{"titre":"Acheter du pain"}'
```

## Tests

```bash
pytest
mypy src/
ruff check .
```

## Publication sur PyPI

```bash
uv build
uv publish       # nécessite UV_PUBLISH_TOKEN
```
