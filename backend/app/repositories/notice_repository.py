from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.notice import Notice
from sqlalchemy.orm import selectinload
from sqlalchemy import or_, and_


from datetime import datetime, timezone
from app.models.notice import ScopeLevel, Visibility, NoticeStatus


class NoticeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Notice | None:
        statement = (
            select(Notice)
            .options(
                selectinload(Notice.department),
                selectinload(Notice.club),
                selectinload(Notice.category),
                selectinload(Notice.course),
                selectinload(Notice.author),
                selectinload(Notice.attachments),
            )
            .where(Notice.id == id)
        )
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def create(self, notice: Notice) -> Notice:
        self.db.add(notice)
        await self.db.commit()
        await self.db.refresh(notice)
        return notice
    async def update(self, notice: Notice) -> Notice:
        await self.db.commit()
        await self.db.refresh(notice)
        return notice

    async def list_all(self, limit: int, offset: int) -> list[Notice]:
        statement = (
            select(Notice)
            .where(Notice.status == NoticeStatus.APPROVED)
            .options(
                selectinload(Notice.department),
                selectinload(Notice.club),
                selectinload(Notice.category),
                selectinload(Notice.course),
                selectinload(Notice.author),
                selectinload(Notice.attachments),
            )
            .order_by(Notice.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def list_by_author(self, author_id: int, limit: int = 50, offset: int = 0) -> list[Notice]:
        statement = (
            select(Notice)
            .where(Notice.author_id == author_id)
            .options(
                selectinload(Notice.category),
                selectinload(Notice.author),
                selectinload(Notice.department),
                selectinload(Notice.club),
                selectinload(Notice.course),
                selectinload(Notice.attachments),
            )
            .order_by(Notice.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def list_for_viewer(
        self,
        department_id: int | None,
        club_ids: list[int],
        course_ids: list[int],
        is_authenticated: bool,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Notice]:
        visibility_conditions = [
            and_(
                Notice.visibility == Visibility.EXTERNAL,
                Notice.scope_level == ScopeLevel.PUBLIC,
            )
        ]

        if is_authenticated:
            visibility_conditions.append(Notice.scope_level == ScopeLevel.PUBLIC)
            visibility_conditions.append(Notice.scope_level == ScopeLevel.CAMPUS)

            if department_id is not None:
                visibility_conditions.append(
                    and_(
                        Notice.scope_level == ScopeLevel.DEPARTMENT,
                        Notice.department_id == department_id,
                    )
                )
            if course_ids:
                visibility_conditions.append(
                    and_(
                        Notice.scope_level == ScopeLevel.COURSE,
                        Notice.course_id.in_(course_ids),
                    )
                )
            if club_ids:
                visibility_conditions.append(
                    and_(
                        Notice.scope_level == ScopeLevel.CLUB,
                        Notice.club_id.in_(club_ids),
                    )
                )

        statement = (
            select(Notice)
            .where(
        Notice.status == NoticeStatus.APPROVED,
        or_(*visibility_conditions),
        or_(
            Notice.expiry_date.is_(None),
            Notice.expiry_date > datetime.now(timezone.utc),
        ),)
            .options(
                selectinload(Notice.category),
                selectinload(Notice.author),
                selectinload(Notice.department),
                selectinload(Notice.club),
                selectinload(Notice.course),
                selectinload(Notice.attachments),
            )
            .order_by(Notice.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())
    async def list_pending(self, limit: int = 50, offset: int = 0) -> list[Notice]:
        statement = (
            select(Notice)
            .where(Notice.status == NoticeStatus.PENDING)
            .options(
                selectinload(Notice.department),
                selectinload(Notice.club),
                selectinload(Notice.category),
                selectinload(Notice.course),
                selectinload(Notice.author),
                selectinload(Notice.attachments),
            )
            .order_by(Notice.created_at.asc())  # oldest pending first — first in, first reviewed
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def list_pinned(self, limit: int = 10) -> list[Notice]:
        statement = (
            select(Notice)
            .where(
                Notice.is_pinned == True,
                Notice.status == NoticeStatus.APPROVED,
                Notice.scope_level == ScopeLevel.PUBLIC,
                Notice.visibility == Visibility.EXTERNAL,
            )
            .options(
                selectinload(Notice.category),
                selectinload(Notice.author),
                selectinload(Notice.department),
                selectinload(Notice.club),
                selectinload(Notice.course),
                selectinload(Notice.attachments),
            )
            .order_by(Notice.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def list_by_category_id(self,category_id: int)-> list[Notice]:
        statement = (select(Notice).where(Notice.category_id == category_id))
        result = await self.db.execute(statement)
        return list(result.scalars().all())

  