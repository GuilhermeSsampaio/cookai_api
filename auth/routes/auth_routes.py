from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from auth.schemas.auth_schema import UserRegister, UserLogin
from auth.schemas.user_schema import UserResponse
from auth.schemas.token_schema import TokenResponse, RefreshTokenRequest
from auth.services.auth_service import safe_create_user, login_user
from auth.security.tokens import create_access_token, create_refresh_token, decode_refresh_token
from fastapi import Depends
from auth.security.dependencies import current_user
from settings.db import SessionDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, session: SessionDep):
    try:
        user = safe_create_user(session, user_data)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already exists",
        )


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, session: SessionDep):
    tokens = login_user(session, credentials.email, credentials.password)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return {**tokens, "token_type": "bearer"}


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(body: RefreshTokenRequest):
    payload = decode_refresh_token(body.refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user_id = payload.get("sub")
    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.get("/protected")
def protected_route(user_id: str = Depends(current_user)):
    return {"message": "protected route accessed", "user_id": user_id}
