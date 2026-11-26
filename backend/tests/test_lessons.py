import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import json
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import init_db, get_db
from app.models import Base, Lesson, Section, Example, Template, DifficultyLevel


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


@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.mark.asyncio
async def test_list_lessons_empty(client: AsyncClient):
    response = await client.get("/api/lessons")
    assert response.status_code == 200
    data = response.json()
    assert "lessons" in data
    assert "total" in data
    assert data["total"] >= 0


@pytest.mark.asyncio
async def test_list_lessons_with_seed(client: AsyncClient):
    # Seed lessons via service
    from app.services.lesson_service import LessonService
    async with TestingSessionLocal() as db:
        await LessonService.seed_lessons(db)

    response = await client.get("/api/lessons")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 5  # We seeded 5 lessons


@pytest.mark.asyncio
async def test_get_lesson_detail(client: AsyncClient):
    from app.services.lesson_service import LessonService
    async with TestingSessionLocal() as db:
        await LessonService.seed_lessons(db)

    response = await client.get("/api/lessons/cli-basics")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "cli-basics"
    assert data["title"] == "CLI Basics"
    assert "sections" in data
    assert len(data["sections"]) >= 1


@pytest.mark.asyncio
async def test_get_nonexistent_lesson(client: AsyncClient):
    response = await client.get("/api/lessons/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_search_lessons(client: AsyncClient):
    from app.services.lesson_service import LessonService
    async with TestingSessionLocal() as db:
        await LessonService.seed_lessons(db)

    response = await client.get("/api/lessons/search?q=cli")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) >= 1
    assert any("cli" in r["title"].lower() for r in data["results"])


@pytest.mark.asyncio
async def test_search_lessons_skill(client: AsyncClient):
    from app.services.lesson_service import LessonService
    async with TestingSessionLocal() as db:
        await LessonService.seed_lessons(db)

    response = await client.get("/api/lessons/search?q=skill")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) >= 1


@pytest.mark.asyncio
async def test_pagination(client: AsyncClient):
    from app.services.lesson_service import LessonService
    async with TestingSessionLocal() as db:
        await LessonService.seed_lessons(db)

    response = await client.get("/api/lessons?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["lessons"]) <= 2
    assert data["page"] == 1
    assert data["page_size"] == 2
@pytest.mark.asyncio
async def test_update_user_progress():
    """Test updating user progress tracking for lesson completion."""
    from app.services.lesson_service import LessonService
    from app.models import UserProgress
    
    async with TestingSessionLocal() as db:
        # First seed lessons to have a lesson_id
        await LessonService.seed_lessons(db)
        
        # Get a lesson ID from the seeded lessons
        result = await db.execute(select(Lesson))
        lessons = result.scalars().all()
        lesson = lessons[0]
        
        # Test: Update progress with some completed sections
        await LessonService.update_user_progress(
            db=db,
            user_id="user-123",
            lesson_id=lesson.id,
            completed_section_ids=["section-1", "section-2"],
        )
        
        # Verify progress was created
        result = await db.execute(
            select(UserProgress).where(
                UserProgress.user_id == "user-123",
                UserProgress.lesson_id == lesson.id,
            )
        )
        progress = result.scalar_one()
        
        assert progress.user_id == "user-123"
        assert progress.lesson_id == lesson.id
        completed = json.loads(progress.completed_sections)
        assert "section-1" in completed
        assert "section-2" in completed
        assert len(completed) == 2
        
        # Test: Update progress again with additional sections (should merge)
        await LessonService.update_user_progress(
            db=db,
            user_id="user-123",
            lesson_id=lesson.id,
            completed_section_ids=["section-3"],
        )
        
        # Verify progress was updated with merged sections
        result = await db.execute(
            select(UserProgress).where(
                UserProgress.user_id == "user-123",
                UserProgress.lesson_id == lesson.id,
            )
        )
        progress = result.scalar_one()
        
        completed = json.loads(progress.completed_sections)
        assert "section-1" in completed
        assert "section-2" in completed
        assert "section-3" in completed
        assert len(completed) == 3
