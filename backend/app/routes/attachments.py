from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.services.attachment_service import AttachmentService
from app.schemas.attachment_schema import AttachmentRead
from app.models.user import User

router = APIRouter(prefix="/notices/{notice_id}/attachments", tags=["attachments"])


@router.post("/", response_model=AttachmentRead)
async def upload_attachment(
    notice_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    attachment_service = AttachmentService(db)
    return await attachment_service.upload(notice_id, file, current_user)