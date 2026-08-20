from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.course_enrollment import CourseEnrollment


class CourseEnrollmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user_id(self, user_id: int) -> list[CourseEnrollment]:
        statement = select(CourseEnrollment).where(CourseEnrollment.user_id == user_id)
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def create(self, course_enrollment: CourseEnrollment) -> CourseEnrollment:
        self.db.add(course_enrollment)
        await self.db.commit()
        await self.db.refresh(course_enrollment)
        return course_enrollment

    async def update(self, enrollment: CourseEnrollment) -> CourseEnrollment:
        await self.db.commit()
        await self.db.refresh(enrollment)
        return enrollment

    async def list_all(self) -> list[CourseEnrollment]:
        statement = select(CourseEnrollment)
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_enrollment(
        self, user_id: int, course_id: int
    ) -> CourseEnrollment | None:
        statement = select(CourseEnrollment).where(
            CourseEnrollment.user_id == user_id, CourseEnrollment.course_id == course_id
        )
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def list_by_course_id(self, course_id: int) -> list[CourseEnrollment]:
        statement = select(CourseEnrollment).where(
            CourseEnrollment.course_id == course_id
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def delete(self, enrollment: CourseEnrollment) -> None:
        await self.db.delete(enrollment)
        await self.db.commit()
