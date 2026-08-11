from datetime import datetime
from pydantic import BaseModel

from app.schemas.notice_schema import NoticeRead


class BookmarkRead(BaseModel):
    user_id: int
    notice_id: int
    created_at: datetime
    notice: NoticeRead

    class Config:
        from_attributes = True