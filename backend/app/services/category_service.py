from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate, CategoryRead
from app.models.category import Category
class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.category_repo = CategoryRepository(db)

    async def create(self, data: CategoryCreate) -> Category:
        return await self.category_repo.create(Category(**data.model_dump()))

    async def list_all(self) -> list[Category]:
        return await self.category_repo.list_all()