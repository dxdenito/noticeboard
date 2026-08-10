from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)

    async def register(self, user_data: UserCreate) -> User:
        # 1. check user_repo.get_by_email — if it exists, raise HTTPException 400
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        # 2. look up the "student" role via role_repo.get_by_name("student")
        student_role = await self.role_repo.get_by_name("student")
        if not student_role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Student role not found",
            )
        # 3. hash the password
        hashed_password = hash_password(user_data.password)
        # 4. build a User(...) object and call user_repo.create_user
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role_id=student_role.id,
            department_id=user_data.department_id,
            is_active=True,
        )
        try:
            await self.user_repo.create_user(new_user)
        except IntegrityError:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error occurred while creating user",
            )

        created_user = await self.user_repo.get_by_email(new_user.email)
        if created_user is None:
            raise HTTPException(status_code=500, detail="User creation failed unexpectedly")

        return created_user

    async def authenticate(self, email: str, password: str) -> User:
        # 1. get user by email — if not found, raise HTTPException 401
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # 2. verify_password — if wrong, raise HTTPException 401 (same message as "not found" — don't reveal which one failed, that leaks which emails are registered)
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # 3. return the user
        return user

    async def update_role(self, user_id: int, role_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")

        role = await self.role_repo.get_by_id(role_id)
        if not role:
            raise HTTPException(400, "Invalid role_id")

        user.role_id = role_id
        return await self.user_repo.update(user)
