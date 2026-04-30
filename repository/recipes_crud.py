from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select
from models.recipe import Recipe


def get_recipe_by_id(session: Session, recipe_id: int) -> Optional[Recipe]:
    return session.get(Recipe, recipe_id)


def list_recipes_by_user_id(session: Session, user_id: UUID) -> List[Recipe]:
    return session.exec(select(Recipe).where(Recipe.user_id == user_id)).all()


def create_recipe(session: Session, recipe: Recipe) -> Recipe:
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe


def update_recipe(session: Session, recipe: Recipe) -> Recipe:
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe


def delete_recipe(session: Session, recipe: Recipe) -> None:
    session.delete(recipe)
    session.commit()
