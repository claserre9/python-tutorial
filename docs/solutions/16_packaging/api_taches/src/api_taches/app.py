from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import engine
from .models import Base
from .routers import auth, taches


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="API Tâches",
        version="0.1.0",
        description="API de gestion de tâches avec auth JWT.",
        lifespan=lifespan,
    )
    app.include_router(auth.router)
    app.include_router(taches.router)
    return app


app = create_app()
