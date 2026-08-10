from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.services.notice_service import NoticeService
from app.schemas.notice_schema import NoticeCreate, NoticeRead
from app.models.user import User
from app.core.deps import get_optional_current_user

router = APIRouter(prefix="/notices", tags=["notices"])


@router.post("/", response_model=NoticeRead)
async def create_notice(
    data: NoticeCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    notice_service = NoticeService(db)
    return await notice_service.create(data, current_user)


from app.core.deps import get_optional_current_user


@router.get("/", response_model=list[NoticeRead])
async def get_feed(
    limit: int = 50,
    offset: int = 0,
    current_user: User | None = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db),
):
    notice_service = NoticeService(db)
    return await notice_service.list_feed(current_user, limit, offset)


@router.get("/{id}", response_model=NoticeRead)
async def get_notice(
    id: int,
    current_user: User | None = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db),
):
    notice_service = NoticeService(db)
    return await notice_service.get_by_id(id, current_user)
