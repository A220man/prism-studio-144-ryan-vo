from app.core.config import settings
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db
from app.models import Base
from app.core.security import create_access_token, decode_token

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_and_decode_token():
    token = create_access_token({"sub": "test-user", "roles": ["viewer", "operator"]})
    assert isinstance(token, str)
    assert len(token) > 0

    decoded = decode_token(token)
    assert decoded is not None
    assert decoded.sub == "test-user"
    assert "viewer" in decoded.roles
    assert "operator" in decoded.roles


@pytest.mark.asyncio
async def test_decode_invalid_token():
    decoded = decode_token("invalid.token.here")
    assert decoded is None


@pytest.mark.asyncio
async def test_decode_expired_token():
    # Create token with past expiration
    from datetime import datetime, timedelta, timezone
    from jose import jwt
    from app.core.config import settings

    expired_token = jwt.encode(
        {"sub": "expired-user", "exp": datetime.now(timezone.utc) - timedelta(hours=1)},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    decoded = decode_token(expired_token)
    assert decoded is None


@pytest.mark.asyncio
async def test_login_endpoint(client: AsyncClient):
    response = await client.get("/api/auth/login")
    assert response.status_code == 200
    data = response.json()
    assert "auth_url" in data
    assert "state" in data
    assert "code_verifier" in data
    assert settings.KEYCLOAK_URL in data["auth_url"]
    assert settings.KEYCLOAK_REALM in data["auth_url"]


@pytest.mark.asyncio
async def test_callback_endpoint(client: AsyncClient):
    response = await client.get("/api/auth/callback?code=test&state=test&code_verifier=test")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client: AsyncClient):
    response = await client.get("/api/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_with_valid_token(client: AsyncClient):
    token = create_access_token({"sub": "test-user", "roles": ["viewer"]})
    response = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["sub"] == "test-user"
    assert data["roles"] == ["viewer"]


@pytest.mark.asyncio
async def test_role_based_access_admin(client: AsyncClient):
    # Viewer token should be forbidden
    viewer_token = create_access_token({"sub": "viewer-user", "roles": ["viewer"]})
    response = await client.get("/api/auth/admin-only", headers={"Authorization": f"Bearer {viewer_token}"})
    assert response.status_code == 403

    # Admin token should succeed
    admin_token = create_access_token({"sub": "admin-user", "roles": ["admin"]})
    response = await client.get("/api/auth/admin-only", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_role_based_access_operator(client: AsyncClient):
    viewer_token = create_access_token({"sub": "viewer-user", "roles": ["viewer"]})
    response = await client.get("/api/auth/operator-only", headers={"Authorization": f"Bearer {viewer_token}"})
    assert response.status_code == 403

    operator_token = create_access_token({"sub": "operator-user", "roles": ["operator"]})
    response = await client.get("/api/auth/operator-only", headers={"Authorization": f"Bearer {operator_token}"})
    assert response.status_code == 200

    admin_token = create_access_token({"sub": "admin-user", "roles": ["admin"]})
    response = await client.get("/api/auth/operator-only", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200