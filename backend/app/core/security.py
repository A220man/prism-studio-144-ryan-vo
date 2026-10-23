from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from pydantic import BaseModel

from app.core.config import settings


class TokenData(BaseModel):
    sub: str
    roles: list[str] = []
    exp: int


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub: str = payload.get("sub")
        roles: list[str] = payload.get("roles", [])
        exp: int = payload.get("exp", 0)
        if sub is None:
            return None
        return TokenData(sub=sub, roles=roles, exp=exp)
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password  # In production, use bcrypt/argon2


def get_password_hash(password: str) -> str:
    return password  # In production, use bcrypt/argon2