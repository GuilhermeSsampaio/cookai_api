from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from settings.settings import GOOGLE_REDIRECT_URI, FRONTEND_URL
from settings.db import SessionDep
from auth.security.google_setup import oauth
from auth.services.oauth_service import get_or_create_oauth_user
from auth.security.tokens import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth/google", tags=["OAuth"])


@router.get("/")
async def google_login(request: Request):
    if not GOOGLE_REDIRECT_URI:
        raise HTTPException(
            status_code=500, detail="GOOGLE_REDIRECT_URI is not configured"
        )

    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI)


@router.get("/callback")
async def google_callback(request: Request, session: SessionDep):
    error_param = request.query_params.get("error")
    if error_param:
        params = urlencode({"error": error_param})
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?{params}")

    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as exc:
        params = urlencode({"error": f"OAuth error: {str(exc)}"})
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?{params}")

    user_info = token.get("userinfo")
    if not user_info:
        params = urlencode({"error": "Missing userinfo from Google"})
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?{params}")

    email = user_info.get("email")
    provider_sub = user_info.get("sub")

    if not email or not provider_sub:
        params = urlencode({"error": "Email or subject not returned"})
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?{params}")

    user = get_or_create_oauth_user(session, email, "google", provider_sub)

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    params = urlencode({"access_token": access_token, "refresh_token": refresh_token})
    return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?{params}")
