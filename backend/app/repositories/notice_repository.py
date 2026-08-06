from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.notice import Notice
from sqlalchemy.orm import selectinload


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

    async def list_all(self, limit: int, offset: int) -> list[Notice]:
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
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())
