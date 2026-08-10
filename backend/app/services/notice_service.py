from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repositories.notice_repository import NoticeRepository
from app.repositories.club_membership_repository import ClubMembershipRepository
from app.repositories.course_enrollment_repository import CourseEnrollmentRepository
from app.models.notice import Notice, ScopeLevel, Visibility
from app.models.user import User
from app.schemas.notice_schema import NoticeCreate


class NoticeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.notice_repo = NoticeRepository(db)
        self.club_membership_repo = ClubMembershipRepository(db)
        self.course_enrollment_repo = CourseEnrollmentRepository(db)

    async def _check_can_post(self, data: NoticeCreate, current_user: User) -> None:
        role = current_user.role.role

        if role == "admin":
            return

        if role == "hod":
            if data.scope_level not in (ScopeLevel.PUBLIC, ScopeLevel.CAMPUS, ScopeLevel.DEPARTMENT):
                raise HTTPException(403, "You don't have permission to post notices")
            if data.scope_level == ScopeLevel.DEPARTMENT and data.department_id != current_user.department_id:
                raise HTTPException(403, "You don't have permission to post notices")
            return

        elif role == "club_leader":
            if data.club_id is None:
                raise HTTPException(403, "You don't have permission to post notices")
            membership = await self.club_membership_repo.get_membership(current_user.id, data.club_id)
            if membership is None or not membership.is_leader:
                raise HTTPException(403, "You don't have permission to post notices")
            return

        elif role == "student_leader":
            if data.course_id is None:
                raise HTTPException(403, "You don't have permission to post notices")
            enrollment = await self.course_enrollment_repo.get_enrollment(current_user.id, data.course_id)
            if enrollment is None or not enrollment.is_leader:
                raise HTTPException(403, "You don't have permission to post notices")
            return

        else:
            raise HTTPException(403, "You don't have permission to post notices")

    async def create(self, data: NoticeCreate, current_user: User) -> Notice:
        await self._check_can_post(data, current_user)

        notice_data = data.model_dump()
        if current_user.role.role == "hod":
            notice_data["department_id"] = current_user.department_id

        new_notice = Notice(**notice_data, author_id=current_user.id)
        return await self.notice_repo.create(new_notice)

    async def list_feed(self, current_user: User | None, limit: int = 50, offset: int = 0) -> list[Notice]:
        if current_user is not None and current_user.role.role == "admin":
            return await self.notice_repo.list_all(limit, offset)

        if current_user is None:
            return await self.notice_repo.list_for_viewer(
                department_id=None, club_ids=[], course_ids=[], is_authenticated=False,
                limit=limit, offset=offset,
            )

        club_memberships = await self.club_membership_repo.list_by_user_id(current_user.id)
        course_enrollments = await self.course_enrollment_repo.list_by_user_id(current_user.id)
        club_ids = [m.club_id for m in club_memberships]
        course_ids = [e.course_id for e in course_enrollments]

        return await self.notice_repo.list_for_viewer(
            department_id=current_user.department_id, club_ids=club_ids, course_ids=course_ids,
            is_authenticated=True, limit=limit, offset=offset,
        )

    async def get_by_id(self, id: int, current_user: User | None) -> Notice:
        notice = await self.notice_repo.get_by_id(id)
        if not notice:
            raise HTTPException(404, "Notice not found")
        if not await self._can_view(notice, current_user):
            raise HTTPException(404, "Notice not found")
        return notice

    async def _can_view(self, notice: Notice, current_user: User | None) -> bool:
        if notice.visibility == Visibility.EXTERNAL and notice.scope_level == ScopeLevel.PUBLIC:
            return True

        if current_user is None:
            return False

        if current_user.role.role == "admin":
            return True

        if notice.scope_level == ScopeLevel.PUBLIC:
            return True
        if notice.scope_level == ScopeLevel.CAMPUS:
            return True

        if notice.scope_level == ScopeLevel.DEPARTMENT:
            return notice.department_id == current_user.department_id

        if notice.scope_level == ScopeLevel.COURSE:
            if notice.course_id is None:
                return False
            enrollment = await self.course_enrollment_repo.get_enrollment(current_user.id, notice.course_id)
            return enrollment is not None

        if notice.scope_level == ScopeLevel.CLUB:
            if notice.club_id is None:
                return False
            membership = await self.club_membership_repo.get_membership(current_user.id, notice.club_id)
            return membership is not None

        return False