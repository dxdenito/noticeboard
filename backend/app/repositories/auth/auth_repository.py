from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload


class AuthRepository:

    def __init__(self, db:AsyncSession):
        self.db=db

    async def get_by_id(self,id:int):
        try:
            statement = select(User).where(User.id == id)
            result = await self.db.execute(statement)
            return result.scalars.first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed. could not search by email"
            )

    async def get_by_email(self, email:str):
        try:
            statement= select(User).where(User.email == email)
            result = await self.db.execute(statement)
            return result.scalars.first()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed. Could not search by email "
            )

    async def create_user(self, user:userCreate)
