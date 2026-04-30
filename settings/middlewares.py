from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from settings.settings import SECRET_KEY, HTTPS_ONLY, CORS_ORIGINS


def _parse_origins(raw_origins: str) -> list[str]:
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def setup_middlewares(app: FastAPI) -> None:
    origins = _parse_origins(CORS_ORIGINS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=bool(origins),
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        SessionMiddleware,
        secret_key=SECRET_KEY,
        same_site="lax",
        https_only=HTTPS_ONLY,
    )
