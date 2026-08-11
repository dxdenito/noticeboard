from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.core.deps import get_optional_current_user
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


from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession


from app.repositories.attachment_repository import AttachmentRepository
from app.services.notice_service import NoticeService
from app.models.user import User

router = APIRouter(prefix="/attachments", tags=["attachments"])


@router.get("/{id}/download")
async def download_attachment(
    id: int,
    current_user: User | None = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db),
):
    attachment_repo = AttachmentRepository(db)
    attachment = await attachment_repo.get_by_id(id)
    if not attachment:
        raise HTTPException(404, "Attachment not found")

    # Reuse the notice's own visibility rules — you can't see the file
    # unless you could see the notice it belongs to.
    notice_service = NoticeService(db)
    await notice_service.get_by_id(attachment.notice_id, current_user)

    return FileResponse(
        path=attachment.file_url,
        filename=attachment.file_name,
        media_type=attachment.content_type,
    )