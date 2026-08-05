from app.core.database import Base
from sqlalchemy import Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.course import Course


class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"


    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, primary_key=True
    )
    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("courses.id"), nullable=False, primary_key=True
    )
    is_leader: Mapped[bool] = mapped_column(default=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="course_enrollments")
    course: Mapped["Course"] = relationship("Course", back_populates="enrollments")
