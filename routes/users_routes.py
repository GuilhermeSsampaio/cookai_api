from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from auth.security.dependencies import current_user
from auth.models.user import User
from auth.schemas.user_schema import UserResponse, UserUpdate
from auth.repository.crud import get_user_by_id
from settings.db import SessionDep

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def me(session: SessionDep, user_id: str = Depends(current_user)):
    user = get_user_by_id(session, UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=UserResponse)
def update_me(
    updates: UserUpdate,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    user = get_user_by_id(session, UUID(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if updates.username is not None:
        user.username = updates.username
    if updates.bios is not None:
        user.bios = updates.bios
    if updates.premium_member is not None:
        user.premium_member = updates.premium_member

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409, detail="Username or email already exists"
        )

    return user


@router.get("/", response_model=List[UserResponse])
def list_users(session: SessionDep, _: str = Depends(current_user)):
    return session.exec(select(User)).all()
