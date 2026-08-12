from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.bookmark_repository import BookmarkRepository
from app.services.notice_service import NoticeService
from app.models.bookmark import Bookmark
from app.models.user import User


class BookmarkService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.bookmark_repo = BookmarkRepository(db)
        self.notice_service = NoticeService(db)

    async def bookmark(self, notice_id: int, current_user: User) -> Bookmark:
        await self.notice_service.get_by_id(notice_id, current_user)

        existing_bookmark = await self.bookmark_repo.get(current_user.id, notice_id)
        if existing_bookmark:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Notice already bookmarked",
            )

        bookmark = Bookmark(user_id=current_user.id, notice_id=notice_id)
        await self.bookmark_repo.create(bookmark)

        reloaded = await self.bookmark_repo.get(current_user.id, notice_id)
        if reloaded is None:
            raise HTTPException(
                status_code=500, detail="Bookmark creation failed unexpectedly"
            )
        return reloaded

    async def unbookmark(self, notice_id: int, current_user: User) -> None:
        existing_bookmark = await self.bookmark_repo.get(current_user.id, notice_id)
        if not existing_bookmark:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found"
            )
        return await self.bookmark_repo.delete(existing_bookmark)

    async def list_my_bookmarks(self, current_user: User) -> list[Bookmark]:
        return list(await self.bookmark_repo.list_by_user_id(current_user.id))