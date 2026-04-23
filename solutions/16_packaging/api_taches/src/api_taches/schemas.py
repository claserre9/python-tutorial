from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TacheIn(BaseModel):
    titre: str = Field(min_length=1, max_length=200)


class TacheOut(BaseModel):
    id: int
    titre: str
    terminee: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
