from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.club_membership_repository import ClubMembershipRepository
from app.repositories.club_repository import ClubRepository
from app.models.club_membership import ClubMembership
from app.models.user import User


class ClubMembershipService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.membership_repo = ClubMembershipRepository(db)
        self.club_repo = ClubRepository(db)

    async def add_member(
        self, club_id: int, user_id: int, current_user: User
    ) -> ClubMembership:

        if not await self.club_repo.get_by_id(club_id):
            raise HTTPException(404, "Club not found")
        if current_user.role.role != "admin":
            membership = await self.membership_repo.get_membership(
                current_user.id, club_id
            )
            if not membership or not membership.is_leader:
                raise HTTPException(403, "Only an admin or club leader can add members")

        existing_membership = await self.membership_repo.get_membership(
            user_id, club_id
        )
        if existing_membership:
            raise HTTPException(400, "User is already a member of this club")

        new_membership = ClubMembership(
            club_id=club_id, user_id=user_id, is_leader=False
        )
        return await self.membership_repo.create(new_membership)

    async def set_leader(
        self, club_id: int, user_id: int, is_leader: bool, current_user: User
    ) -> ClubMembership:

        if current_user.role.role != "admin":
            raise HTTPException(403, "Only an admin can assign club leadership")
        membership = await self.membership_repo.get_membership(user_id, club_id)
        if membership is None:
            raise HTTPException(404, "Membership not found")
        membership.is_leader = is_leader
        # you'll need a ClubMembershipRepository.update() method — same shape as the others
        return await self.membership_repo.update(membership)
