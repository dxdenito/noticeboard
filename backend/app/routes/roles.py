from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_roles, get_db
from app.services.role_service import RoleService
from app.schemas.role_schema import RoleRead
from app.models.user import User

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=list[RoleRead])
async def list_roles(
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    service = RoleService(db)
    return await service.list_all()