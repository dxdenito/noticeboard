from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repositories.course_repository import CourseRepository
from app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from app.models.course import Course
from app.models.user import User
from app.schemas.course_schema import CourseCreate, CourseUpdate



class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.course_repo = CourseRepository(db)
        self.enrollment_repo = CourseEnrollmentRepository(db)

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

    async def remove_all_enrollments(self, current_user:User, course_id: int)->None:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise HTTPException(
                404,
                "Course not found"
            )
        if current_user.role.role != "admin":
            raise HTTPException(
                403,"You have no permission to update this course"
            )
        enrollments = await self.enrollment_repo.list_by_course_id(course_id)
        for enrollment in enrollments:
            await self.enrollment_repo.delete(enrollment)


    async def delete(self, current_user: User, course_id: int) -> None:
        if current_user.role.role != "admin":
            raise HTTPException(403, "Forbidden, not allowed to delete")

        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise HTTPException(404, "Course not found")

        enrollments = await self.enrollment_repo.list_by_course_id(course_id)
        if enrollments:
            raise HTTPException(400, f"Cannot delete this course: {len(enrollments)} enrollment(s) still attached. Remove them first.")

        await self.course_repo.delete(course)


