from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.category_schema import CategoryRead, CategoryCreate
from app.services.category_service import CategoryService
from app.models.user import User
from app.core.deps import require_roles
from app.core.database import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryRead)
async def create_category(
    data: CategoryCreate,
    current_user: User = Depends(require_roles("admin")),
    db=Depends(get_db),
):
    return await CategoryService(db).create(data)


@router.get("/", response_model=list[CategoryRead])
async def list_categories(db=Depends(get_db)):  # public, same reasoning as departments
    return await CategoryService(db).list_all()

@router.patch("/{id}/reassign-notices")
async def reassign_category_notices(
    id: int,
    to_category_id: int,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    category_service = CategoryService(db)
    return await category_service.reassign_notices(id, to_category_id)


@router.delete("/{id}", status_code=204)
async def delete_category(
    id: int,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    category_service = CategoryService(db)
    await category_service.delete(current_user, id)
