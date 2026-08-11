from datetime import datetime
from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.notice import Notice


class Bookmark(Base):
    __tablename__ = "bookmarks"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    notice_id: Mapped[int] = mapped_column(ForeignKey("notices.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="bookmarks")
    notice: Mapped["Notice"] = relationship(back_populates="bookmarked_by")