from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.role_repository import RoleRepository
from app.models.role import Role


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.role_repo = RoleRepository(db)

    async def list_all(self) -> list[Role]:
        return await self.role_repo.list_all()