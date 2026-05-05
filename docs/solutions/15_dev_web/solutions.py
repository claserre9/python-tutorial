"""
Solutions — Chapitre 15
"""
from datetime import datetime

import pytest
from fastapi import FastAPI, Depends, HTTPException
from httpx import AsyncClient, ASGITransport
from pydantic import BaseModel, EmailStr, Field


app = FastAPI()


# 15.1 — Produits
class ProduitOut(BaseModel):
    id: int
    nom: str
    prix: float


@app.get("/produits/{id}")
async def get_produit(id: int) -> ProduitOut:
    if id < 1:
        raise HTTPException(404, "produit introuvable")
    return ProduitOut(id=id, nom="Exemple", prix=9.99)


# 15.2 — Users
class UserIn(BaseModel):
    nom: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


class UserOut(BaseModel):
    id: int
    nom: str
    email: EmailStr
    age: int
    created_at: datetime


@app.post("/users", status_code=201)
async def creer_user(user: UserIn) -> UserOut:
    return UserOut(
        id=1,
        nom=user.nom,
        email=user.email,
        age=user.age,
        created_at=datetime.now(),
    )


# 15.3 — Items + Depends
FAKE_DB: dict[int, dict] = {}


class ItemIn(BaseModel):
    nom: str = Field(min_length=1)


class ItemOut(BaseModel):
    id: int
    nom: str


def get_db() -> dict[int, dict]:
    return FAKE_DB


@app.post("/items", status_code=201)
async def creer_item(item: ItemIn, db: dict = Depends(get_db)) -> ItemOut:
    new_id = (max(db.keys(), default=0)) + 1
    db[new_id] = {"id": new_id, "nom": item.nom}
    return ItemOut(id=new_id, nom=item.nom)


@app.get("/items/{id}")
async def get_item(id: int, db: dict = Depends(get_db)) -> ItemOut:
    if id not in db:
        raise HTTPException(404, "item introuvable")
    return ItemOut(**db[id])


# Tests
@pytest.mark.asyncio
async def test_get_produit():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/produits/1")
        assert r.status_code == 200


@pytest.mark.asyncio
async def test_user_invalide():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/users", json={"nom": "", "email": "x", "age": 200})
        assert r.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
