# Chapitre 15 — Dev web moderne avec FastAPI

Construire une API HTTP/JSON professionnelle avec **FastAPI** (async), **Pydantic v2** pour la validation, **SQLAlchemy 2.0** (async) pour la persistance, authentification **JWT**, tests avec `httpx.AsyncClient`. Tout le paquet moderne.

## 1. Pourquoi FastAPI

- **Async natif** : exploite `asyncio` (Ch. 12).
- **Typage = validation** : Pydantic lit vos annotations et valide automatiquement.
- **Docs auto** : OpenAPI + Swagger UI générés.
- **Injection de dépendances** propre.
- **Performance** comparable à Go/Node (ASGI + uvicorn).

## 2. Rappels HTTP/REST

| Méthode | Sémantique |
|---|---|
| `GET /users/{id}` | Lire une ressource |
| `GET /users` | Lister / filtrer |
| `POST /users` | Créer |
| `PUT /users/{id}` | Remplacer intégralement |
| `PATCH /users/{id}` | Modifier partiellement |
| `DELETE /users/{id}` | Supprimer |

Codes de statut :
- `2xx` : succès (`200` OK, `201` Created, `204` No Content)
- `4xx` : erreur client (`400` Bad Request, `401` Unauthorized, `404` Not Found, `409` Conflict, `422` Unprocessable Entity)
- `5xx` : erreur serveur (`500`, `502`, `503`)

## 3. Hello, FastAPI

```bash
uv pip install fastapi uvicorn
```

```python
# app.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello"}


@app.get("/users/{id}")
async def get_user(id: int):
    return {"id": id, "nom": "Alice"}
```

Lancer :

```bash
uvicorn app:app --reload
```

Puis :
- `http://localhost:8000` : l'API
- `http://localhost:8000/docs` : Swagger UI (auto-généré)
- `http://localhost:8000/redoc` : ReDoc

## 4. Pydantic v2 — validation

Pydantic lit vos annotations et génère des modèles validés.

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserIn(BaseModel):
    nom: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


class UserOut(BaseModel):
    id: int
    nom: str
    email: EmailStr
    created_at: datetime
```

### `Field` — contraintes fines

```python
from pydantic import Field

class Produit(BaseModel):
    nom: str = Field(min_length=1, max_length=200)
    prix: float = Field(gt=0)
    tags: list[str] = Field(default_factory=list, max_length=10)
    description: str | None = Field(default=None, description="Texte libre")
```

### Validation custom

```python
from pydantic import model_validator, field_validator

class Commande(BaseModel):
    debut: datetime
    fin: datetime

    @model_validator(mode="after")
    def verif_dates(self):
        if self.fin <= self.debut:
            raise ValueError("fin doit être > debut")
        return self
```

### Exploitation dans une route

```python
@app.post("/users", response_model=UserOut, status_code=201)
async def creer(user: UserIn) -> UserOut:
    # user est déjà validé : email bien formé, age dans les bornes, etc.
    return UserOut(id=1, nom=user.nom, email=user.email, created_at=datetime.now())
```

Une requête invalide (mauvais email, age négatif...) retourne automatiquement **422 Unprocessable Entity** avec un JSON décrivant les champs en erreur. Aucun code à écrire.

## 5. Query params, path params, body

```python
from fastapi import Query, Path

@app.get("/users")
async def lister(
    q: str | None = Query(default=None, max_length=50),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
) -> list[UserOut]:
    ...


@app.get("/users/{user_id}/posts/{post_id}")
async def get_post(
    user_id: int = Path(ge=1),
    post_id: int = Path(ge=1),
):
    ...
```

## 6. Dépendances (DI)

Les **Depends** sont le mécanisme de FastAPI pour injecter des objets dans les routes : DB session, utilisateur courant, config, etc.

```python
from fastapi import Depends

async def get_db():
    async with SessionLocal() as session:
        yield session


@app.get("/users/{id}")
async def get_user(id: int, db = Depends(get_db)):
    return await db.get(User, id)
```

La dépendance peut avoir ses propres dépendances (graphe). Elle est **résolue par requête** (instance fraîche à chaque appel).

### Dépendance pour l'auth

```python
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="/token")

async def current_user(token: str = Depends(oauth2), db = Depends(get_db)) -> User:
    user = decode_jwt_and_get_user(token, db)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return user


@app.get("/me")
async def me(user: User = Depends(current_user)) -> UserOut:
    return user
```

Toute route qui injecte `current_user` est automatiquement protégée.

## 7. Gestion d'erreurs

Lever `HTTPException` pour les erreurs attendues :

```python
from fastapi import HTTPException

@app.get("/users/{id}")
async def get_user(id: int, db = Depends(get_db)) -> UserOut:
    user = await db.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user
```

Pour une gestion globale d'exceptions métier :

```python
@app.exception_handler(MaBusinessException)
async def handler(request, exc):
    return JSONResponse(status_code=400, content={"error": str(exc)})
```

## 8. SQLAlchemy 2.0 async

```bash
uv pip install "sqlalchemy[asyncio]" asyncpg
```

### Modèles

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): ...

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
```

### Engine et session async

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db", echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
```

### Requêtes

```python
from sqlalchemy import select

async with SessionLocal() as session:
    # Par clé
    user = await session.get(User, 1)

    # Requête
    stmt = select(User).where(User.email == "a@a.com")
    user = (await session.scalars(stmt)).one_or_none()

    # Liste
    users = (await session.scalars(select(User).limit(10))).all()

    # Insert
    new = User(nom="Alice", email="a@a.com")
    session.add(new)
    await session.commit()
```

### Alternative : SQLModel

Unifie Pydantic et SQLAlchemy :

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nom: str
    email: str
```

Moins de duplication, adapté aux cas simples. SQLAlchemy pur reste plus flexible.

## 9. Auth JWT

```bash
uv pip install pyjwt passlib[bcrypt]
```

### Générer / valider

```python
import jwt
from datetime import datetime, timedelta

SECRET = "..."
ALGO = "HS256"

def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=[ALGO])
```

### Route de login

```python
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    user = await authenticate(form.username, form.password, db)
    if not user:
        raise HTTPException(401, "credentials invalid")
    return {"access_token": create_token(user.id), "token_type": "bearer"}
```

### Hasher les mots de passe

```python
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"])

hashed = pwd_ctx.hash("mon_mdp")
pwd_ctx.verify("mon_mdp", hashed)     # True
```

**Ne jamais** stocker les mots de passe en clair. Toujours hasher.

## 10. Background tasks

```python
from fastapi import BackgroundTasks

def envoyer_email(email: str, corps: str):
    # ... SMTP
    ...


@app.post("/users")
async def creer(user: UserIn, bg: BackgroundTasks):
    # ... créer user en DB
    bg.add_task(envoyer_email, user.email, "bienvenue")
    return {"ok": True}
```

Pour des tâches plus lourdes / fiables : **Celery**, **RQ**, **Dramatiq** ou un worker async dédié.

## 11. CORS

Pour autoriser un frontend sur un domaine différent :

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 12. Tests avec httpx

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app import app


@pytest.mark.asyncio
async def test_creer_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/users", json={"nom": "Alice", "email": "a@a.com", "age": 30})
        assert r.status_code == 201
        assert r.json()["nom"] == "Alice"
```

`ASGITransport` : on teste l'app **en mémoire** sans démarrer un serveur. Rapide et hermétique.

Pour la DB : base SQLite temporaire par test, ou fixtures avec `tmp_path` + migration.

## 13. OpenAPI / Swagger

FastAPI génère automatiquement :

- `/docs` : Swagger UI
- `/redoc` : ReDoc
- `/openapi.json` : schéma OpenAPI 3 brut

Vous pouvez l'enrichir :

```python
app = FastAPI(
    title="Mon API",
    version="1.0.0",
    description="Documentation de l'API.",
    contact={"name": "Support", "email": "support@example.com"},
)
```

---

## Projet fil rouge (voir Ch. 16)

Le projet **API fil rouge** du Niveau 3 combine ce chapitre + le suivant : une API FastAPI complète, testée, packagée et publiée sur PyPI. Implémentation dans le dossier `solutions/16_packaging/api_taches/`.

---

### Piège courant : routes sync dans une app async

```python
@app.get("/lent")
def lent():                      # ❌ sync dans une app async
    time.sleep(5)
    return {"ok": True}
```

FastAPI exécute les routes `def` dans un thread pool, donc ça ne bloque pas tout, mais c'est inefficace et source de confusion. Règle : routes toujours `async def` dans une app async.

---

### Sous le capot : ASGI

Les apps FastAPI sont des apps **ASGI** (successeur async de WSGI). Uvicorn est un serveur ASGI. L'interface minimale :

```python
async def app(scope, receive, send):
    # scope = infos de la requête
    # receive = coroutine pour lire le body
    # send = coroutine pour répondre
    ...
```

Tout FastAPI est construit au-dessus. Starlette (la lib sous-jacente) implémente le routeur et middleware, FastAPI ajoute Pydantic, DI et OpenAPI.

---

## À retenir

- Routes `async def`, Pydantic pour valider, type hints partout.
- `Depends` pour l'injection (DB, auth, config...).
- `HTTPException` pour les erreurs attendues.
- SQLAlchemy 2.0 async ou SQLModel pour la persistance.
- JWT + `OAuth2PasswordBearer` pour l'auth.
- Tests via `httpx.AsyncClient` + `ASGITransport`.

---

➡️ [Chapitre 16 — Packaging & distribution](../16_packaging/README.md)
