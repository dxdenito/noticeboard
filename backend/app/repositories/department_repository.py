from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.department import Department


class DepartmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Department | None:
        statement = select(Department).where(Department.id == id)
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def get_by_code(self, code: str) -> Department | None:
        statement = select(Department).where(Department.code == code)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, department: Department) -> Department:
        self.db.add(department)
        await self.db.commit()
        await self.db.refresh(department)
        return department

    async def update(self, department: Department) -> Department:
        await self.db.commit()
        await self.db.refresh(department)
        return department
    async def delete(self, department: Department) -> None:
        await self.db.delete(department)
        await self.db.commit()

    async def list_all(self) -> list[Department]:
        statement = select(Department)
        result = await self.db.execute(statement)
        return list(result.scalars().all())
