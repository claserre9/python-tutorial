from httpx import AsyncClient


async def test_register(client: AsyncClient):
    r = await client.post("/register", json={"email": "a@a.com", "password": "longpass1"})
    assert r.status_code == 201
    assert r.json()["email"] == "a@a.com"


async def test_register_dup(client: AsyncClient):
    await client.post("/register", json={"email": "a@a.com", "password": "longpass1"})
    r = await client.post("/register", json={"email": "a@a.com", "password": "longpass1"})
    assert r.status_code == 409


async def test_login_ok(client: AsyncClient):
    await client.post("/register", json={"email": "a@a.com", "password": "longpass1"})
    r = await client.post(
        "/token",
        data={"username": "a@a.com", "password": "longpass1"},
    )
    assert r.status_code == 200
    assert "access_token" in r.json()


async def test_login_mauvais_mdp(client: AsyncClient):
    await client.post("/register", json={"email": "a@a.com", "password": "longpass1"})
    r = await client.post(
        "/token",
        data={"username": "a@a.com", "password": "mauvais"},
    )
    assert r.status_code == 401


async def test_route_protegee(client: AsyncClient):
    r = await client.get("/taches")
    assert r.status_code == 401
