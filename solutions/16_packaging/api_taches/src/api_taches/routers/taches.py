from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import current_user
from ..db import get_db
from ..models import Tache, User
from ..schemas import TacheIn, TacheOut


router = APIRouter(prefix="/taches", tags=["taches"])


@router.get("", response_model=list[TacheOut])
async def lister(
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Tache]:
    stmt = select(Tache).where(Tache.owner_id == user.id)
    return list((await db.scalars(stmt)).all())


@router.post("", response_model=TacheOut, status_code=201)
async def creer(
    payload: TacheIn,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> Tache:
    tache = Tache(titre=payload.titre, owner_id=user.id)
    db.add(tache)
    await db.commit()
    await db.refresh(tache)
    return tache


@router.post("/{tache_id}/done", response_model=TacheOut)
async def marquer_done(
    tache_id: int,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> Tache:
    tache = await db.get(Tache, tache_id)
    if not tache or tache.owner_id != user.id:
        raise HTTPException(404, "tâche introuvable")
    tache.terminee = True
    await db.commit()
    await db.refresh(tache)
    return tache


@router.delete("/{tache_id}", status_code=204)
async def supprimer(
    tache_id: int,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    tache = await db.get(Tache, tache_id)
    if not tache or tache.owner_id != user.id:
        raise HTTPException(404, "tâche introuvable")
    await db.delete(tache)
    await db.commit()
