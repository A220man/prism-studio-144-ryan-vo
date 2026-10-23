from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from urllib.parse import urlencode
import secrets

from app.core.config import settings
from app.core.security import create_access_token
from app.api.deps import get_current_user, require_roles

router = APIRouter(tags=["auth"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


@router.get("/login")
async def login():
    """Initiate OIDC PKCE login flow."""
    state = secrets.token_urlsafe(32)
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = code_verifier  # In production, use S256 hash

    # Store in session (simplified - use proper session storage)
    # For now, return the auth URL
    params = {
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "response_type": "code",
        "scope": "openid profile email roles",
        "redirect_uri": "http://localhost:5173/callback",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    auth_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth?{urlencode(params)}"
    return {"auth_url": auth_url, "state": state, "code_verifier": code_verifier}


@router.get("/callback")
async def callback(code: str, state: str, code_verifier: str):
    """Handle OIDC callback and exchange code for tokens."""
    # In production, verify state matches, exchange code with Keycloak
    # For demo, return a mock token
    access_token = create_access_token(
        data={"sub": "demo-user", "roles": ["viewer"]}
    )
    return TokenResponse(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/logout")
async def logout():
    return {"message": "Logged out"}


@router.get("/me")
async def get_current_user_info(current_user = Depends(get_current_user)):
    return {"sub": current_user.sub, "roles": current_user.roles}


@router.get("/admin-only")
async def admin_only(current_user = Depends(require_roles("admin"))):
    return {"message": "Admin access granted", "user": current_user.sub}


@router.get("/operator-only")
async def operator_only(current_user = Depends(require_roles("operator", "admin"))):
    return {"message": "Operator access granted", "user": current_user.sub}