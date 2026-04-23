from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import create_token, hash_password, verify_password
from ..db import get_db
from ..models import User
from ..schemas import Token, UserIn, UserOut


router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(user: UserIn, db: AsyncSession = Depends(get_db)) -> User:
    existing = await db.scalar(select(User).where(User.email == user.email))
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "email déjà utilisé")

    new_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/token", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    user = await db.scalar(select(User).where(User.email == form.username))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "credentials invalid")
    return Token(access_token=create_token(user.id))
