from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Index
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class DifficultyLevel(str, PyEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String(64), primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(64), nullable=False)
    difficulty = Column(Enum(DifficultyLevel), nullable=False, default=DifficultyLevel.BEGINNER)
    estimated_minutes = Column(Integer, nullable=False, default=10)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    sections = relationship("Section", back_populates="lesson", cascade="all, delete-orphan", order_by="Section.order")

    __table_args__ = (
        Index("ix_lessons_category", "category"),
        Index("ix_lessons_difficulty", "difficulty"),
    )


class Section(Base):
    __tablename__ = "sections"

    id = Column(String(64), primary_key=True)
    lesson_id = Column(String(64), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(256), nullable=False)
    content = Column(Text, nullable=False)
    order = Column(Integer, nullable=False, default=0)

    lesson = relationship("Lesson", back_populates="sections")
    examples = relationship("Example", back_populates="section", cascade="all, delete-orphan", order_by="Example.order")
    templates = relationship("Template", back_populates="section", cascade="all, delete-orphan", order_by="Template.order")


class Example(Base):
    __tablename__ = "examples"

    id = Column(String(64), primary_key=True)
    section_id = Column(String(64), ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(256), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(32), nullable=False, default="yaml")
    order = Column(Integer, nullable=False, default=0)

    section = relationship("Section", back_populates="examples")


class Template(Base):
    __tablename__ = "templates"

    id = Column(String(64), primary_key=True)
    section_id = Column(String(64), ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(256), nullable=False)
    content = Column(Text, nullable=False)
    filename = Column(String(256), nullable=False)
    order = Column(Integer, nullable=False, default=0)

    section = relationship("Section", back_populates="templates")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    lesson_id = Column(String(64), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    completed_sections = Column(Text, nullable=False, default="[]")
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_user_progress_user_lesson", "user_id", "lesson_id", unique=True),
    )