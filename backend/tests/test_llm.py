import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db
from app.models import Base
from app.services.llm_service import LLMService

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
async def test_llm_service_lists_providers():
    service = LLMService()
    providers = service.list_providers()
    assert "openai-compatible" in providers
    assert "anthropic" in providers
    assert "gemini" in providers
    assert "ollama" in providers
    assert len(providers) == 4


@pytest.mark.asyncio
async def test_llm_service_get_provider():
    service = LLMService()
    provider = service.get_provider("openai-compatible")
    assert provider is not None
    assert hasattr(provider, "generate")
    assert hasattr(provider, "is_configured")


@pytest.mark.asyncio
async def test_llm_service_invalid_provider():
    service = LLMService()
    with pytest.raises(ValueError):
        service.get_provider("invalid-provider")


@pytest.mark.asyncio
async def test_ollama_provider_configured():
    service = LLMService()
    provider = service.get_provider("ollama")
    assert provider.is_configured() is True


@pytest.mark.asyncio
async def test_openai_provider_not_configured_without_key():
    # Default settings have no API key
    service = LLMService()
    provider = service.get_provider("openai-compatible")
    assert provider.is_configured() is False