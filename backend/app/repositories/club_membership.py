from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.club_membership import ClubMembership


class ClubMembershipRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user_id(self, user_id: int) -> list[ClubMembership]:
        statement = select(ClubMembership).where(ClubMembership.user_id == user_id)
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def create(self, club_membership: ClubMembership) -> ClubMembership:
        self.db.add(club_membership)
        await self.db.commit()
        await self.db.refresh(club_membership)
        return club_membership

    async def list_all(self) -> list[ClubMembership]:
        statement = select(ClubMembership)
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_membership(self, user_id: int, club_id: int) -> ClubMembership | None:
        statement = select(ClubMembership).where(
            ClubMembership.user_id == user_id, ClubMembership.club_id == club_id
        )
        result = await self.db.execute(statement)
        return result.scalars().first()
