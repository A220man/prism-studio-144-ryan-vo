from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List

from app.core.database import get_db
from app.services.lesson_service import LessonService
from app.models import Lesson, Section, Example, Template, DifficultyLevel

router = APIRouter(tags=["lessons"])


class LessonResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    difficulty: str
    estimated_minutes: int

    class Config:
        from_attributes = True


class ExampleResponse(BaseModel):
    id: str
    title: str
    code: str
    language: str

    class Config:
        from_attributes = True


class TemplateResponse(BaseModel):
    id: str
    title: str
    content: str
    filename: str

    class Config:
        from_attributes = True


class SectionResponse(BaseModel):
    id: str
    title: str
    content: str
    examples: List[ExampleResponse] = []
    templates: List[TemplateResponse] = []

    class Config:
        from_attributes = True


class LessonDetailResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    difficulty: str
    estimated_minutes: int
    sections: List[SectionResponse] = []

    class Config:
        from_attributes = True


class PaginatedLessonsResponse(BaseModel):
    lessons: List[LessonResponse]
    total: int
    page: int
    page_size: int


@router.get("", response_model=PaginatedLessonsResponse)
async def list_lessons(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    diff = DifficultyLevel(difficulty) if difficulty else None
    lessons, total = await LessonService.list_lessons(
        db, page=page, page_size=page_size, category=category, difficulty=diff, search=search
    )
    return {
        "lessons": [LessonResponse.model_validate(l) for l in lessons],
        "total": total,
        "page": page,
        "page_size": page_size,
    }

@router.get("/search")
async def search_lessons(q: str = "", limit: int = Query(10, ge=1, le=50), db: AsyncSession = Depends(get_db)):
    lessons = await LessonService.search_lessons(db, q, limit)
    return {"results": [LessonResponse.model_validate(l) for l in lessons], "total": len(lessons)}


@router.get("/{lesson_id}", response_model=LessonDetailResponse)
async def get_lesson(lesson_id: str, db: AsyncSession = Depends(get_db)):
    lesson = await LessonService.get_lesson(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    sections = []
    for section in lesson.sections:
        sections.append(SectionResponse(
            id=section.id,
            title=section.title,
            content=section.content,
            examples=[ExampleResponse.model_validate(e) for e in section.examples],
            templates=[TemplateResponse.model_validate(t) for t in section.templates],
        ))

    return LessonDetailResponse(
        id=lesson.id,
        title=lesson.title,
        description=lesson.description,
        category=lesson.category,
        difficulty=lesson.difficulty.value,
        estimated_minutes=lesson.estimated_minutes,
        sections=sections,
    )