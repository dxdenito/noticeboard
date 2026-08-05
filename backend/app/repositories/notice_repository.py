from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.notice import Notice


class NoticeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Notice | None:
        statement = select(Notice).where(Notice.id == id)
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def create(self, notice: Notice) -> Notice:
        self.db.add(notice)
        await self.db.commit()
        await self.db.refresh(notice)
        return notice

    async def list_all(self) -> list[Notice]:
        statement = select(Notice)
        result = await self.db.execute(statement)
        return list(result.scalars().all())