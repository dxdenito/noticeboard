from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.bookmark import Bookmark
from app.models.notice import Notice


class BookmarkRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, user_id: int, notice_id: int) -> Bookmark | None:
        statement = (
            select(Bookmark)
            .where(Bookmark.user_id == user_id, Bookmark.notice_id == notice_id)
            .options(
                selectinload(Bookmark.notice).selectinload(Notice.category),
                selectinload(Bookmark.notice).selectinload(Notice.author),
                selectinload(Bookmark.notice).selectinload(Notice.department),
                selectinload(Bookmark.notice).selectinload(Notice.club),
                selectinload(Bookmark.notice).selectinload(Notice.course),
                selectinload(Bookmark.notice).selectinload(Notice.attachments),
            )
        )
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def create(self, bookmark: Bookmark) -> Bookmark:
        self.db.add(bookmark)
        await self.db.commit()
        await self.db.refresh(bookmark)
        return bookmark

    async def delete(self, bookmark: Bookmark) -> None:
        await self.db.delete(bookmark)
        await self.db.commit()

    async def list_by_user_id(self, user_id: int) -> list[Bookmark]:
        statement = (
            select(Bookmark)
            .where(Bookmark.user_id == user_id)
            .options(
                selectinload(Bookmark.notice).selectinload(Notice.category),
                selectinload(Bookmark.notice).selectinload(Notice.author),
                selectinload(Bookmark.notice).selectinload(Notice.department),
                selectinload(Bookmark.notice).selectinload(Notice.club),
                selectinload(Bookmark.notice).selectinload(Notice.course),
                selectinload(Bookmark.notice).selectinload(Notice.attachments),
            )
            .order_by(Bookmark.created_at.desc())
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())