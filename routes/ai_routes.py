from typing import List

from fastapi import APIRouter, HTTPException

from schemas.ai_schema import AiRecipeResponse, ScrapeRequest, SearchRequest
from services.ai.scrapping import scrap_recipe
from services.ai.web_search import search_recipes_from_web

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/scrap", response_model=AiRecipeResponse)
def scrap(data: ScrapeRequest):
    result = scrap_recipe(data.url)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/search", response_model=List[AiRecipeResponse])
def search(data: SearchRequest):
    result = search_recipes_from_web(data.query)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=500, detail=result["error"])
    return result
