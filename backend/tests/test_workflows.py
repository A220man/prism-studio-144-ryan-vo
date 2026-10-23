import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db
from app.models import Base
from app.services.workflow_service import WorkflowService


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
async def test_list_workflows(client: AsyncClient):
    response = await client.get("/api/workflows")
    assert response.status_code == 200
    data = response.json()
    assert "workflows" in data
    assert len(data["workflows"]) == 3
    workflow_ids = {w["id"] for w in data["workflows"]}
    assert workflow_ids == {"skill-wizard", "subagent-builder", "mcp-configurator"}


@pytest.mark.asyncio
async def test_skill_wizard_generates_valid_yaml(client: AsyncClient):
    response = await client.post(
        "/api/workflows/skill-wizard",
        json={
            "name": "test-skill",
            "description": "A test skill",
            "model": "sonnet",
            "tools": "bash,read,write",
            "allowed_tools": "bash,read",
            "example": "do something",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "template" in data
    template = data["template"]
    assert "name: test-skill" in template
    assert "description: A test skill" in template
    assert "model: sonnet" in template
    assert "tools: bash,read,write" in template
    assert "allowed-tools: bash,read" in template
    assert "/test-skill do something" in template


@pytest.mark.asyncio
async def test_skill_wizard_minimal_fields(client: AsyncClient):
    response = await client.post(
        "/api/workflows/skill-wizard",
        json={"name": "minimal-skill", "description": "Minimal skill"},
    )
    assert response.status_code == 200
    data = response.json()
    template = data["template"]
    assert "name: minimal-skill" in template
    assert "description: Minimal skill" in template


@pytest.mark.asyncio
async def test_subagent_builder_generates_valid_markdown(client: AsyncClient):
    response = await client.post(
        "/api/workflows/subagent-builder",
        json={
            "name": "code-reviewer",
            "description": "Reviews code",
            "model": "opus",
            "tools": "read,glob,grep",
            "system_prompt": "You are a code reviewer.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    template = data["template"]
    assert "name: code-reviewer" in template
    assert "description: Reviews code" in template
    assert "model: opus" in template
    assert "tools: read,glob,grep" in template
    assert "You are a code reviewer." in template


@pytest.mark.asyncio
async def test_mcp_configurator_generates_valid_json(client: AsyncClient):
    response = await client.post(
        "/api/workflows/mcp-configurator",
        json={
            "name": "filesystem",
            "command": "npx",
            "args": "-y @modelcontextprotocol/server-filesystem /tmp",
            "env": '{"ALLOWED_DIR": "/tmp"}',
            "transport": "stdio",
        },
    )
    assert response.status_code == 200
    data = response.json()
    template = data["template"]
    assert '"filesystem"' in template
    assert '"command": "npx"' in template
    assert '"args"' in template
    assert '@modelcontextprotocol/server-filesystem' in template
    assert '"ALLOWED_DIR"' in template


@pytest.mark.asyncio
async def test_mcp_configurator_minimal(client: AsyncClient):
    response = await client.post(
        "/api/workflows/mcp-configurator",
        json={"name": "minimal-server", "command": "python", "args": "-m myserver"},
    )
    assert response.status_code == 200
    data = response.json()
    template = data["template"]
    assert '"minimal-server"' in template
    assert '"command": "python"' in template


@pytest.mark.asyncio
async def test_workflow_service_unit():
    skill = WorkflowService.generate_skill({
        "name": "unit-test",
        "description": "Unit test skill",
        "model": "haiku",
        "tools": "read,write",
        "allowed_tools": "read",
        "example": "test",
    })
    assert "name: unit-test" in skill
    assert "model: haiku" in skill

    subagent = WorkflowService.generate_subagent({
        "name": "test-agent",
        "description": "Test agent",
        "model": "sonnet",
        "tools": "read",
        "system_prompt": "Test prompt",
    })
    assert "name: test-agent" in subagent
    assert "Test prompt" in subagent

    mcp = WorkflowService.generate_mcp_config({
        "name": "test-mcp",
        "command": "node",
        "args": "server.js",
        "env": '{}',
        "transport": "stdio",
    })
    assert '"test-mcp"' in mcp
    assert '"command": "node"' in mcp