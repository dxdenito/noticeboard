# app/services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.models.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)

    async def update_role(self, user_id: int, role_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")

        role = await self.role_repo.get_by_id(role_id)
        if not role:
            raise HTTPException(400, "Invalid role_id")

        if role.role == "hod" and user.department_id is None:
            raise HTTPException(
                400, "Cannot assign the HOD role to a user with no department set"
            )

        user.role_id = role_id
        return await self.user_repo.update(user)
