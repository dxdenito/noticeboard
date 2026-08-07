from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repositories.course_repository import CourseRepository
from app.models.course import Course
from app.models.user import User
from app.schemas.course_schema import CourseCreate, CourseUpdate


class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.course_repo = CourseRepository(db)

    async def create(self, data: CourseCreate) -> Course:
        new_course = Course(**data.model_dump())
        return await self.course_repo.create(new_course)

    async def list_all(self) -> list[Course]:
        return await self.course_repo.list_all()

    async def get_by_id(self, id: int) -> Course:
        course = await self.course_repo.get_by_id(id)
        if not course:
            raise HTTPException(404, "Course not found")
        return course

    async def update(self, id: int, data: CourseUpdate, current_user: User) -> Course:
        course = await self.course_repo.get_by_id(id)
        if not course:
            raise HTTPException(404, "Course not found")

        if current_user.role.role != "admin":
            if (
                current_user.role.role != "hod"
                or current_user.department_id != course.department_id
            ):
                raise HTTPException(
                    403, "You don't have permission to update this course"
                )

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(course, field, value)
        return await self.course_repo.update(course)
