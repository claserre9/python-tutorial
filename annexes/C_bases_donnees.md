# Annexe C — Bases de données

De `sqlite3` (stdlib, 100% fiable) à SQLAlchemy (ORM industriel). Ce qu'il faut savoir pour choisir et utiliser sans se tromper.

## 1. `sqlite3` — la base en stdlib

SQLite est une DB relationnelle **embarquée** (pas de serveur). Stockée dans un fichier. Incluse avec Python.

```python
import sqlite3
from pathlib import Path

conn = sqlite3.connect("app.db")
cur = conn.cursor()

# DDL
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT UNIQUE
    )
""")

# Insertion avec paramètres — JAMAIS de f-string !
cur.execute("INSERT INTO users (nom, email) VALUES (?, ?)", ("Alice", "a@a.com"))
conn.commit()

# Sélection
cur.execute("SELECT id, nom FROM users WHERE email = ?", ("a@a.com",))
row = cur.fetchone()          # (1, "Alice")

cur.execute("SELECT id, nom FROM users")
rows = cur.fetchall()         # [(1, "Alice"), ...]

conn.close()
```

### Context manager

```python
with sqlite3.connect("app.db") as conn:
    # commit automatique à la sortie normale, rollback si exception
    cur = conn.execute("INSERT INTO users VALUES (?, ?)", (None, "Bob"))
```

### `Row` factory — accès par nom

```python
conn.row_factory = sqlite3.Row
row = conn.execute("SELECT * FROM users LIMIT 1").fetchone()
row["nom"]            # au lieu de row[1]
```

### Migrations

`sqlite3` n'a pas de migrations — c'est à vous de gérer. Pour du sérieux : **Alembic** (vient avec SQLAlchemy).

## 2. Injection SQL — le piège mortel

```python
# ❌ JAMAIS
nom = input("nom ? ")
cur.execute(f"SELECT * FROM users WHERE nom = '{nom}'")   # injection possible

# Input malicieux : Bob'; DROP TABLE users;--
# La table est détruite.

# ✅ TOUJOURS paramétré
cur.execute("SELECT * FROM users WHERE nom = ?", (nom,))
```

Cette règle s'applique à **tous** les drivers (psycopg, mysqlclient, SQLAlchemy raw...). Utilisez toujours le paramétrage du driver.

## 3. SQLAlchemy 2.0 — l'ORM industriel

Utilisé pour les projets réels, multiplateforme (PostgreSQL, MySQL, SQLite...).

### Synchrone minimal

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


engine = create_engine("sqlite:///app.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(engine)

with Session() as session:
    # Insert
    u = User(nom="Alice", email="a@a.com")
    session.add(u)
    session.commit()

    # Query
    user = session.scalar(select(User).where(User.email == "a@a.com"))
```

### Async (voir Ch. 15)

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///app.db")
Session = async_sessionmaker(engine, expire_on_commit=False)

async with Session() as session:
    await session.execute(select(User))
```

### Relations

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    titre: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped[User] = relationship(back_populates="posts")


class User(Base):
    # ...
    posts: Mapped[list[Post]] = relationship(back_populates="author", cascade="all, delete-orphan")
```

### N+1 problem

```python
# ❌ N+1 requêtes : 1 pour users + 1 par user pour ses posts
users = session.scalars(select(User)).all()
for u in users:
    for p in u.posts:    # nouvelle requête à chaque fois !
        ...
```

Solution : `selectinload` / `joinedload` :

```python
from sqlalchemy.orm import selectinload

users = session.scalars(select(User).options(selectinload(User.posts))).all()
# 2 requêtes au total
```

Toujours surveiller les logs avec `echo=True` en dev.

## 4. Alembic — migrations

```bash
uv pip install alembic
alembic init migrations
```

`alembic.ini` : configurez `sqlalchemy.url`.

`migrations/env.py` : pointez `target_metadata = Base.metadata`.

```bash
# Générer une migration depuis les changements de modèle
alembic revision --autogenerate -m "add email to users"

# Appliquer
alembic upgrade head

# Revenir en arrière
alembic downgrade -1
```

Toujours **relire** les migrations auto-générées (Alembic rate parfois des indexes, constraints, etc.).

## 5. SQLModel — alternative légère

Par l'auteur de FastAPI, unifie Pydantic + SQLAlchemy :

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nom: str
    email: str = Field(unique=True)
```

Simple mais moins flexible que SQLAlchemy pur pour les cas complexes. Bon pour un prototype ou petit projet.

## 6. Choisir son driver PostgreSQL

Pour Postgres (le choix standard en prod) :

- **`psycopg`** (v3) : sync, moderne, bonne API.
- **`asyncpg`** : async, le plus rapide en Python.
- **`psycopg2-binary`** : l'historique. Fonctionne, mais préférez psycopg 3 pour les nouveaux projets.

Avec SQLAlchemy :

```python
# sync
"postgresql+psycopg://user:pass@host/db"

# async
"postgresql+asyncpg://user:pass@host/db"
```

## 7. Connection pooling

SQLAlchemy gère un pool par défaut. Pour configurer :

```python
create_engine(url, pool_size=10, max_overflow=20, pool_pre_ping=True)
```

- `pool_pre_ping` : vérifie la connexion avant usage (évite les "connection gone away" après un restart DB).
- `pool_recycle=3600` : recycle les connexions après N secondes.

## 8. Transactions

```python
with Session() as session:
    with session.begin():      # ouvre une transaction
        session.add(user1)
        session.add(user2)
        # commit automatique à la sortie, rollback si exception
```

Ou explicite :

```python
try:
    session.add(...)
    session.commit()
except Exception:
    session.rollback()
    raise
```

## 9. Types Python → SQL

SQLAlchemy 2.0 infère le type SQL depuis l'annotation Python :

| Python | SQL |
|---|---|
| `int` | `INTEGER` |
| `str` | `VARCHAR(...)` ou `TEXT` |
| `float` | `FLOAT` / `DOUBLE` |
| `bool` | `BOOLEAN` |
| `datetime` | `DATETIME` / `TIMESTAMP` |
| `bytes` | `BLOB` / `BYTEA` |
| `list[X]` (Postgres) | `ARRAY` |

## 10. Sans ORM : query builders légers

- **SQL brut + `psycopg`/`sqlite3`** : simple, explicite, idéal pour du code ad hoc.
- **Peewee** : ORM plus simple que SQLAlchemy, API proche de Django.
- **Tortoise ORM** : async-first, inspiré de Django.

## Règle

Pour un nouveau projet backend :

- Petit, prototype : SQLite + SQLAlchemy 2.0.
- Prod : Postgres + SQLAlchemy + Alembic.
- API ultra-rapide : asyncpg + requêtes SQL manuelles (bypass ORM).
