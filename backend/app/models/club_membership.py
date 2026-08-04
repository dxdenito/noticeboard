from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.club import Club

class ClubMembership(Base):
    __tablename__ = "club_memberships"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, index=True
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"),primary_key=True)
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey("clubs.id"), primary_key=True)
    is_leader:Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    club:Mapped["Club"] = relationship("Club", back_populates = "memberships")
    user:Mapped["User"] = relationship("User", back_populates= "club_memberships")

    