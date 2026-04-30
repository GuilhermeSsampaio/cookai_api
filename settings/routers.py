from fastapi import FastAPI
from auth.routes.auth_routes import router as auth_router
from auth.routes.oauth_routes import router as oauth_router
from routes.users_routes import router as users_router
from routes.recipes_routes import router as recipes_router
from routes.ai_routes import router as ai_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(oauth_router)
    app.include_router(users_router)
    app.include_router(recipes_router)
    app.include_router(ai_router)
