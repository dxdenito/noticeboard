from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.club_membership_repository import ClubMembershipRepository
from app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.department_repository import DepartmentRepository
from app.models.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
        self.department_repo = DepartmentRepository(db)
        self.club_membership_repo = ClubMembershipRepository(db)
        self.course_enrollment_repo = CourseEnrollmentRepository(db)

    async def update_role(self, user_id: int, role_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")

        role = await self.role_repo.get_by_id(role_id)
        if not role:
            raise HTTPException(400, "Invalid role_id")

        if role.role == "hod" and user.department_id is None:
            raise HTTPException(400, "Cannot assign HOD to a user with no department set")

        if role.role == "club_leader":
            memberships = await self.club_membership_repo.list_by_user_id(user_id)
            if not memberships:
                raise HTTPException(400, "Cannot assign club_leader to a user with no club membership")

        if role.role == "student_leader":
            enrollments = await self.course_enrollment_repo.list_by_user_id(user_id)
            if not enrollments:
                raise HTTPException(400, "Cannot assign student_leader to a user with no course enrollment")

        user.role_id = role_id
        return await self.user_repo.update(user)
    async def update_department(self, user_id: int, department_id: int | None) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")

        if department_id is not None:
            department = await self.department_repo.get_by_id(department_id)
            if not department:
                raise HTTPException(400, "Invalid department_id")

        user.department_id = department_id
        return await self.user_repo.update(user)