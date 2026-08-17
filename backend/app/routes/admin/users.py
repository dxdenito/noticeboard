from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_roles, get_db
from app.services.admin.user_admin_service import UserAdminService
from app.schemas.user_schema import UserRead
from app.models.user import User

router = APIRouter(prefix="/admin/users", tags=["admin"])


# in the route
@router.get("/", response_model=list[UserRead])
async def list_users(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    service = UserAdminService(db)
    return await service.list_users(limit, offset)


@router.patch("/{id}/deactivate", response_model=UserRead)
async def deactivate_user(
    id: int,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    service = UserAdminService(db)
    return await service.set_active_status(id, False)


@router.patch("/{id}/activate", response_model=UserRead)
async def activate_user(
    id: int,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    service = UserAdminService(db)
    return await service.set_active_status(id, True)
