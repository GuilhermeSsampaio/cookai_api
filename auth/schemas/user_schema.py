from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    bios: Optional[str] = None
    premium_member: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    bios: Optional[str] = None
    premium_member: Optional[bool] = None
