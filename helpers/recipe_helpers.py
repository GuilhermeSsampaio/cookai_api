from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session

from models.recipe import Recipe
from repository.recipes_crud import get_recipe_by_id


def get_recipe_or_404(session: Session, recipe_id: int) -> Recipe:
    recipe = get_recipe_by_id(session, recipe_id)

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe


def check_ownership(recipe: Recipe, user_id: UUID) -> None:
    if recipe.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission for this recipe",
        )
