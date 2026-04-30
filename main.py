from contextlib import asynccontextmanager
from fastapi import FastAPI

from settings.db import create_db_and_tables
from settings.settings import API_TITLE, API_VERSION
from settings.middlewares import setup_middlewares
from settings.routers import setup_routers


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title=API_TITLE, version=API_VERSION, lifespan=lifespan)

setup_middlewares(app)
setup_routers(app)


@app.get("/")
def root():
    return {"message": "CookAi API"}
