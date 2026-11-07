from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from urllib.parse import urlencode
import secrets
import hashlib
import base64
import httpx

from app.core.config import settings
from app.core.security import create_access_token, decode_token, TokenData
from app.api.deps import get_current_user, require_roles

router = APIRouter(tags=["auth"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Simple in-memory store for PKCE code verifiers (use Redis in production)
pkce_store: dict[str, str] = {}


def generate_code_challenge(code_verifier: str) -> str:
    """Generate S256 code challenge from code verifier."""
    digest = hashlib.sha256(code_verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")


@router.get("/login")
async def login(response: Response):
    """Initiate OIDC PKCE login flow."""
    state = secrets.token_urlsafe(32)
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = generate_code_challenge(code_verifier)

    # Store code verifier with state as key (expires in 10 minutes)
    pkce_store[state] = code_verifier

    # Set state in secure httpOnly cookie
    response.set_cookie(
        "oauth_state",
        state,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        max_age=600,  # 10 minutes
    )

    params = {
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "response_type": "code",
        "scope": "openid profile email roles",
        "redirect_uri": f"{settings.CORS_ORIGINS[0]}/callback",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    auth_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth?{urlencode(params)}"
    return {"auth_url": auth_url}


@router.get("/callback")
async def callback(code: str, state: str, request: Request, response: Response):
    """Handle OIDC callback and exchange code for tokens with Keycloak."""
    # Verify state matches
    stored_state = request.cookies.get("oauth_state")
    if not stored_state or stored_state != state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    # Retrieve and remove code verifier
    code_verifier = pkce_store.pop(state, None)
    if not code_verifier:
        raise HTTPException(status_code=400, detail="Invalid or expired PKCE challenge")

    # Clear state cookie
    response.delete_cookie("oauth_state")

    # Exchange authorization code for tokens with Keycloak
    token_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    token_data = {
        "grant_type": "authorization_code",
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        "code": code,
        "redirect_uri": f"{settings.CORS_ORIGINS[0]}/callback",
        "code_verifier": code_verifier,
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=token_data)

    if token_response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Token exchange failed: {token_response.text}",
        )

    tokens = token_response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    id_token = tokens.get("id_token")
    expires_in = tokens.get("expires_in", settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    if not access_token:
        raise HTTPException(status_code=400, detail="No access token received")

    # Set tokens in secure httpOnly cookies
    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        max_age=expires_in,
    )
    if refresh_token:
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            secure=settings.ENVIRONMENT == "production",
        samesite="lax",
            max_age=60 * 60 * 24 * 30,  # 30 days
        )

    # Redirect to frontend
    return RedirectResponse(url=f"{settings.CORS_ORIGINS[0]}/")


@router.post("/logout")
async def logout(response: Response):
    """Clear session cookies."""
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}


@router.get("/me")
async def get_current_user_info(current_user: TokenData = Depends(get_current_user)):
    return {"sub": current_user.sub, "roles": current_user.roles}


@router.get("/admin-only")
async def admin_only(current_user: TokenData = Depends(require_roles("admin"))):
    return {"message": "Admin access granted", "user": current_user.sub}


@router.get("/operator-only")
async def operator_only(current_user: TokenData = Depends(require_roles("operator", "admin"))):
    return {"message": "Operator access granted", "user": current_user.sub}