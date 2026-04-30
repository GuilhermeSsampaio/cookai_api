from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID

if TYPE_CHECKING:
    from auth.models.user import User


class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    font: str
    link: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user_id: UUID = Field(foreign_key="user.id", index=True)
    user: Optional["User"] = Relationship(back_populates="recipes")
