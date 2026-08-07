import enum
from datetime import datetime

from sqlalchemy import Integer, DateTime, func, String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.user import User
    from app.models.department import Department
    from app.models.club import Club
    from app.models.course import Course
    from app.models.attachment import Attachment


class Priority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ScopeLevel(enum.Enum):
    PUBLIC = "public"
    DEPARTMENT = "department"
    COURSE = "course"
    CAMPUS = "campus"
    CLUB = "club"


class Visibility(enum.Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"


class Notice(Base):
    __tablename__ = "notices"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id"), nullable=False
    )
    course_id: Mapped[int | None] = mapped_column(
        ForeignKey("courses.id"), nullable=True
    )
    club_id: Mapped[int | None] = mapped_column(
        ForeignKey("clubs.id"), nullable=True
    )

    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    scope_level: Mapped[ScopeLevel] = mapped_column(
        Enum(ScopeLevel, native_enum=False), nullable=False
    )
    priority: Mapped[Priority] = mapped_column(
        Enum(Priority, native_enum=False), nullable=False
    )
    visibility: Mapped[Visibility] = mapped_column(
        Enum(Visibility, native_enum=False), nullable=False
    )
    department_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("departments.id"), nullable=True
    )

    expiry_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # relationships
    category: Mapped["Category"] = relationship("Category", back_populates="notices")

    author: Mapped["User"] = relationship("User", back_populates="notices")
    department: Mapped["Department | None"] = relationship(
        "Department", back_populates="notices"
    )
    club: Mapped["Club | None"] = relationship("Club", back_populates="notices")
    course: Mapped["Course | None"] = relationship("Course")
    attachments: Mapped[list["Attachment"]] = relationship(
        "Attachment", back_populates="notice"
    )
