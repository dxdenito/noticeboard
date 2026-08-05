from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.role import Role


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Role | None:
        statement = select(Role).where(Role.id == id)
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def get_by_name(self, name: str) -> Role | None:
        statement = select(Role).where(Role.role == name)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, role: Role) -> Role:
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def list_all(self) -> list[Role]:
        statement = select(Role)
        result = await self.db.execute(statement)
        return list(result.scalars().all())
