from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repositories.user_repository import UserRepository
from app.models.user import User


class UserAdminService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def set_active_status(self, user_id: int, is_active: bool) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")

        user.is_active = is_active
        return await self.user_repo.update(user)

    
    async def list_users(self, limit: int = 50, offset: int = 0) -> list[User]:
        return await self.user_repo.list_users(limit, offset)