from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.services.notice_service import NoticeService
from app.schemas.notice_schema import NoticeCreate, NoticeRead
from app.models.user import User

router = APIRouter(prefix="/notices", tags=["notices"])


@router.post("/", response_model=NoticeRead)
async def create_notice(
    data: NoticeCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    notice_service = NoticeService(db)
    return await notice_service.create(data, current_user)