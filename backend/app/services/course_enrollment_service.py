from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.course_enrollment import CourseEnrollment
from app.models.user import User
from app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from app.repositories.course_repository import CourseRepository


class CourseEnrollmentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = CourseEnrollmentRepository(db)
        self.course_repo = CourseRepository(db)

    async def add_enrollment(
        self, course_id: int, user_id: int, current_user: User
    ) -> CourseEnrollment:
        if not await self.course_repo.get_by_id(course_id):
            raise HTTPException(404, "Course not found")

        if current_user.role.role != "admin":
            leader_check = await self.repository.get_enrollment(
                current_user.id, course_id
            )
            if leader_check is None or not leader_check.is_leader:
                raise HTTPException(
                    403, "Only an admin or the course leader can add enrollments"
                )

        existing = await self.repository.get_enrollment(user_id, course_id)
        if existing:
            raise HTTPException(400, "User is already enrolled in this course")

        new_enrollment = CourseEnrollment(
            user_id=user_id, course_id=course_id, is_leader=False
        )
        return await self.repository.create(new_enrollment)

    async def set_leader(
        self, course_id: int, user_id: int, is_leader: bool, current_user: User
    ) -> CourseEnrollment:
        if current_user.role.role != "admin":
            raise HTTPException(403, "Only an admin can assign course leadership")

        enrollment = await self.repository.get_enrollment(user_id, course_id)
        if enrollment is None:
            raise HTTPException(404, "Enrollment not found")

        enrollment.is_leader = is_leader
        return await self.repository.update(enrollment)

    async def list_all_enrollments(self) -> list[CourseEnrollment]:
        return await self.repository.list_all()
