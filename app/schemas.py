from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Role = Literal["admin", "editor", "user"]


# ---------- Auth ----------
class Token(BaseModel):
    access_token: str
    token_type: str


# ---------- Users ----------
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str
    full_name: Optional[str] = None
    password: str = Field(min_length=8)
    role: Role = "user"


class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str
    full_name: Optional[str] = None
    disabled: bool
    role: Role


# ---------- Notes ----------
class NoteCreate(BaseModel):
    title: str = Field(min_length=1)
    content: str
    is_public: bool = False
    tags: List[str] = []


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_public: Optional[bool] = None
    tags: Optional[List[str]] = None


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    owner: str
    is_public: bool
    created_at: datetime
    tags: List[str]
