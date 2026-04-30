from uuid import UUID
from sqlmodel import Session

from helpers.recipe_helpers import check_ownership, get_recipe_or_404
from models.recipe import Recipe
from repository.recipes_crud import (
    create_recipe,
    delete_recipe,
    list_recipes_by_user_id,
    update_recipe,
)
from schemas.recipe_schema import RecipeCreate, RecipeUpdate


def save_recipe_for_user(
    session: Session, user_id: UUID, recipe_data: RecipeCreate
) -> Recipe:
    new_recipe = Recipe(
        title=recipe_data.title,
        content=recipe_data.content,
        font=recipe_data.font,
        link=recipe_data.link,
        user_id=user_id,
    )

    return create_recipe(session, new_recipe)


def list_user_recipes(session: Session, user_id: UUID) -> list[Recipe]:
    return list_recipes_by_user_id(session, user_id)


def update_user_recipe(
    session: Session, user_id: UUID, recipe_id: int, data: RecipeUpdate
) -> Recipe:
    recipe = get_recipe_or_404(session, recipe_id)
    check_ownership(recipe, user_id)

    if data.title is not None:
        recipe.title = data.title
    if data.content is not None:
        recipe.content = data.content

    return update_recipe(session, recipe)


def delete_user_recipe(session: Session, user_id: UUID, recipe_id: int) -> str:
    recipe = get_recipe_or_404(session, recipe_id)
    check_ownership(recipe, user_id)

    title = recipe.title
    delete_recipe(session, recipe)
    return title
