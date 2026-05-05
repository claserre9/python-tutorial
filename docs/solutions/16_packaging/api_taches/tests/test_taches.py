from httpx import AsyncClient


async def test_creer_et_lister(auth_client: AsyncClient):
    r = await auth_client.post("/taches", json={"titre": "Acheter du pain"})
    assert r.status_code == 201
    tid = r.json()["id"]

    r = await auth_client.get("/taches")
    assert r.status_code == 200
    taches = r.json()
    assert len(taches) == 1
    assert taches[0]["titre"] == "Acheter du pain"
    assert taches[0]["terminee"] is False


async def test_marquer_done(auth_client: AsyncClient):
    r = await auth_client.post("/taches", json={"titre": "X"})
    tid = r.json()["id"]

    r = await auth_client.post(f"/taches/{tid}/done")
    assert r.status_code == 200
    assert r.json()["terminee"] is True


async def test_supprimer(auth_client: AsyncClient):
    r = await auth_client.post("/taches", json={"titre": "X"})
    tid = r.json()["id"]

    r = await auth_client.delete(f"/taches/{tid}")
    assert r.status_code == 204

    r = await auth_client.get("/taches")
    assert r.json() == []


async def test_titre_vide(auth_client: AsyncClient):
    r = await auth_client.post("/taches", json={"titre": ""})
    assert r.status_code == 422


async def test_isolation_utilisateurs(client: AsyncClient):
    """Les tâches d'un user ne doivent pas être visibles par un autre."""
    # User 1 crée une tâche
    await client.post("/register", json={"email": "u1@x.com", "password": "longpass1"})
    r1 = await client.post("/token", data={"username": "u1@x.com", "password": "longpass1"})
    token1 = r1.json()["access_token"]
    await client.post("/taches", json={"titre": "privée"}, headers={"Authorization": f"Bearer {token1}"})

    # User 2 n'en voit aucune
    await client.post("/register", json={"email": "u2@x.com", "password": "longpass1"})
    r2 = await client.post("/token", data={"username": "u2@x.com", "password": "longpass1"})
    token2 = r2.json()["access_token"]
    r = await client.get("/taches", headers={"Authorization": f"Bearer {token2}"})
    assert r.json() == []
