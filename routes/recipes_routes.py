from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from auth.security.dependencies import current_user
from schemas.recipe_schema import RecipeCreate, RecipeResponse, RecipeUpdate
from services.recipe_service import (
    save_recipe_for_user,
    list_user_recipes,
    update_user_recipe,
    delete_user_recipe,
)
from settings.db import SessionDep

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.post("/", response_model=RecipeResponse)
def create_recipe(
    recipe_data: RecipeCreate,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    return save_recipe_for_user(session, UUID(user_id), recipe_data)


@router.get("/", response_model=List[RecipeResponse])
def list_recipes(session: SessionDep, user_id: str = Depends(current_user)):
    return list_user_recipes(session, UUID(user_id))


@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_data: RecipeUpdate,
    session: SessionDep,
    recipe_id: int,
    user_id: str = Depends(current_user),
):
    return update_user_recipe(session, UUID(user_id), recipe_id, recipe_data)


@router.delete("/{recipe_id}")
def delete_recipe(
    session: SessionDep,
    recipe_id: int,
    user_id: str = Depends(current_user),
):
    title = delete_user_recipe(session, UUID(user_id), recipe_id)
    return {"message": f"Recipe '{title}' deleted"}
