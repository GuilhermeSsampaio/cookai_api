import os
from dotenv import load_dotenv

load_dotenv()

API_TITLE = os.getenv("API_TITLE", "CookAi API")
API_VERSION = os.getenv("API_VERSION", "1.0.0")

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-dev")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cookai.db")
RESET_DB = os.getenv("RESET_DB", "false").strip().lower() == "true"

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback"
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", FRONTEND_URL)
HTTPS_ONLY = os.getenv("HTTPS_ONLY", "false").strip().lower() == "true"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GENAI_MODEL = os.getenv("GENAI_MODEL", "gemini-2.5-flash")
