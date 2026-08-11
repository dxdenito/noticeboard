from fastapi import APIRouter, Depends
from app.core.deps import get_current_user, require_roles
from app.models.user import User
from app.schemas.user_schema import UserRead, UserRoleUpdate, UserDepartmentUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.bookmark_service import BookmarkService
from app.schemas.bookmark_schema import BookmarkRead


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/me/bookmarks", response_model=list[BookmarkRead])
async def get_my_bookmarks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    bookmark_service = BookmarkService(db)
    return await bookmark_service.list_my_bookmarks(current_user)

@router.patch("/{id}/role", response_model=UserRead)
async def update_user_role(
    id: int,
    data: UserRoleUpdate,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    auth_service = AuthService(db)
    return await auth_service.update_role(id, data.role_id)

@router.patch("/{id}/department", response_model=UserRead)
async def update_user_department(
    id: int,
    data: UserDepartmentUpdate,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    user_service = UserService(db)
    return await user_service.update_department(id, data.department_id)


