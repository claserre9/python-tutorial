from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api_taches.app import create_app
from api_taches.db import get_db
from api_taches.models import Base


@pytest.fixture
async def app_and_db(tmp_path) -> AsyncIterator:
    url = f"sqlite+aiosqlite:///{tmp_path}/test.db"
    engine = create_async_engine(url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    yield app
    await engine.dispose()


@pytest.fixture
async def client(app_and_db) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app_and_db),
        base_url="http://test",
    ) as c:
        yield c


@pytest.fixture
async def auth_client(client: AsyncClient) -> AsyncIterator[AsyncClient]:
    await client.post("/register", json={"email": "u@ex.com", "password": "secret123"})
    r = await client.post(
        "/token",
        data={"username": "u@ex.com", "password": "secret123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = r.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    yield client
