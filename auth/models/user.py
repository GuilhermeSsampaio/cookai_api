from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import List, Optional, TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from auth.models.auth_provider import AuthProvider
    from models.recipe import Recipe


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    is_active: bool = Field(default=True)
    bios: Optional[str] = None
    premium_member: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    providers: List["AuthProvider"] = Relationship(back_populates="user")
    recipes: List["Recipe"] = Relationship(back_populates="user")
