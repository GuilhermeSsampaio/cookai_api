from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RecipeCreate(BaseModel):
    title: str
    content: str
    font: str
    link: str


class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class RecipeResponse(BaseModel):
    id: int
    title: str
    content: str
    font: str
    link: str
    created_at: datetime
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)
