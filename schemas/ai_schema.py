from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    url: str


class SearchRequest(BaseModel):
    query: str


class AiRecipeResponse(BaseModel):
    title: str
    font: str
    link: str
    content: str
    duration_ms: int | None = None
