from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repositories.notice_repository import NoticeRepository
from app.repositories.club_membership_repository import ClubMembershipRepository
from app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from app.models.notice import Notice, ScopeLevel
from app.models.user import User
from app.schemas.notice_schema import NoticeCreate


class NoticeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.notice_repo = NoticeRepository(db)
        self.club_membership_repo = ClubMembershipRepository(db)
        self.course_enrollment_repo = CourseEnrollmentRepository(db)

    async def _check_can_post(self, data: NoticeCreate, current_user: User) -> None:
        """Raises HTTPException(403) if current_user isn't allowed to post
        this specific notice (given its scope_level and target). Returns
        nothing on success — does NOT create anything."""
        role = current_user.role.role

        if role == "admin":
            return  # admin can post anything, no further checks

        if role == "hod":
            if data.scope_level != ScopeLevel.DEPARTMENT:
                raise HTTPException(403, "You don't have permission to post notices")
            if data.department_id != current_user.department_id:
                raise HTTPException(403, "You don't have permission to post notices")
            return

        elif role == "club_leader":
            if data.club_id is None:
                raise HTTPException(403, "You don't have permission to post notices")
            membership = await self.club_membership_repo.get_membership(
                current_user.id, data.club_id
            )
            if membership is None or not membership.is_leader:
                raise HTTPException(403, "You don't have permission to post notices")
            return

        elif role == "student_leader":
            if data.course_id is None:
                raise HTTPException(403, "You don't have permission to post notices")
            enrollment = await self.course_enrollment_repo.get_enrollment(
                current_user.id, data.course_id
            )
            if enrollment is None or not enrollment.is_leader:
                raise HTTPException(403, "You don't have permission to post notices")
            return

        else:
            raise HTTPException(403, "You don't have permission to post notices")

    async def create(self, data: NoticeCreate, current_user: User) -> Notice:
        await self._check_can_post(data, current_user)

        new_notice = Notice(
            **data.model_dump(),
            author_id=current_user.id,
        )
        return await self.notice_repo.create(new_notice)
