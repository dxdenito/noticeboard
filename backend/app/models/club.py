from datetime import datetime
from sqlalchemy import Integer, String, func, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.club_membership import ClubMembership
    from app.models.notice import Notice


class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    memberships: Mapped[list["ClubMembership"]] = relationship(
        "ClubMembership", back_populates="club", cascade="all, delete-orphan"
    )
    notices: Mapped[list["Notice"]] = relationship(back_populates="club")
