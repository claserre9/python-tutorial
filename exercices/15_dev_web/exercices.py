"""
Exercices — Chapitre 15 : FastAPI

Ces exercices se font dans une mini-app FastAPI.
Installez : uv pip install fastapi uvicorn httpx pytest-asyncio pydantic[email]
"""
from datetime import datetime

import pytest
from fastapi import FastAPI, Depends, HTTPException
from httpx import AsyncClient, ASGITransport
from pydantic import BaseModel, EmailStr, Field


# =============================================================================
# 15.1 — Route GET simple avec Pydantic
# =============================================================================
# Créez une app FastAPI avec :
#  - GET /produits/{id} qui retourne un ProduitOut (id, nom, prix)
#  - Si id < 1, lever HTTPException 404.

app = FastAPI()


class ProduitOut(BaseModel):
    ...  # TODO


@app.get("/produits/{id}")
async def get_produit(id: int) -> ProduitOut:
    ...  # TODO


# =============================================================================
# 15.2 — POST avec validation Pydantic
# =============================================================================
# POST /users : accepte UserIn (nom min 1 char, email valide, age 0-150).
# Retourne UserOut (id=1, les champs du user, created_at).

class UserIn(BaseModel):
    ...  # TODO : nom, email, age avec contraintes


class UserOut(BaseModel):
    id: int
    nom: str
    email: EmailStr
    age: int
    created_at: datetime


@app.post("/users", status_code=201)
async def creer_user(user: UserIn) -> UserOut:
    ...  # TODO


# =============================================================================
# 15.3 — Depends : fake DB
# =============================================================================
# Implémentez une "DB" en mémoire (dict) injectée via Depends.
# Routes :
#  - POST /items : ajoute un item (id auto)
#  - GET /items/{id} : récupère, 404 si absent

FAKE_DB: dict[int, dict] = {}


class ItemIn(BaseModel):
    nom: str = Field(min_length=1)


class ItemOut(BaseModel):
    id: int
    nom: str


def get_db() -> dict[int, dict]:
    ...  # TODO : retourner FAKE_DB


@app.post("/items", status_code=201)
async def creer_item(item: ItemIn, db: dict = Depends(get_db)) -> ItemOut:
    ...  # TODO


@app.get("/items/{id}")
async def get_item(id: int, db: dict = Depends(get_db)) -> ItemOut:
    ...  # TODO : 404 si absent


# =============================================================================
# 15.4 — Tests avec httpx
# =============================================================================

@pytest.mark.asyncio
async def test_get_produit():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/produits/1")
        assert r.status_code == 200
        assert r.json()["id"] == 1

        r = await c.get("/produits/0")
        assert r.status_code == 404


@pytest.mark.asyncio
async def test_creer_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/users", json={"nom": "Alice", "email": "a@a.com", "age": 30})
        assert r.status_code == 201
        assert r.json()["nom"] == "Alice"


@pytest.mark.asyncio
async def test_user_invalide():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/users", json={"nom": "", "email": "mauvais", "age": 200})
        assert r.status_code == 422


@pytest.mark.asyncio
async def test_items_crud():
    FAKE_DB.clear()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/items", json={"nom": "Livre"})
        assert r.status_code == 201
        item_id = r.json()["id"]

        r = await c.get(f"/items/{item_id}")
        assert r.status_code == 200
        assert r.json()["nom"] == "Livre"

        r = await c.get("/items/99999")
        assert r.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
