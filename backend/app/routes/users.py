from fastapi import APIRouter, Depends
from app.core.deps import get_current_user, require_roles
from app.models.user import User
from app.schemas.user_schema import UserRead, UserRoleUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.auth_service import AuthService


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/{id}/role", response_model=UserRead)
async def update_user_role(
    id: int,
    data: UserRoleUpdate,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    auth_service = AuthService(db)
    return await auth_service.update_role(id, data.role_id)
