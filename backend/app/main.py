from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api import health, lessons, workflows, auth
from app.services.lesson_service import LessonService
from app.core.database import get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    # Seed initial lessons
    async with get_session() as db:
        await LessonService.seed_lessons(db)
    yield
    # Shutdown
    await close_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Prism Studio API",
        version="1.0.0",
        description="Visual, example-driven guide to Claude Code",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/api")
    app.include_router(auth.router, prefix="/api/auth")
    app.include_router(lessons.router, prefix="/api/lessons")
    app.include_router(workflows.router, prefix="/api/workflows")

    return app


app = create_app()