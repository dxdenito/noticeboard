from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.club_repository import ClubRepository
from app.repositories.club_membership_repository import ClubMembershipRepository
from app.models.club import Club
from app.models.user import User
from app.schemas.club_schema import ClubCreate, ClubUpdate
from fastapi import HTTPException


class ClubService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.club_repo = ClubRepository(db)
        self.membership_repo = ClubMembershipRepository(db)

    async def create(self, data: ClubCreate) -> Club:
        new_club = Club(**data.model_dump())
        return await self.club_repo.create(new_club)

    async def list_all(self) -> list[Club]:
        return await self.club_repo.list_all()

    async def get_by_id(self, id: int) -> Club:
        # 404 if missing
        club = await self.club_repo.get_by_id(id)
        if not club:
            raise HTTPException(404, "Club not found")
        return club

    async def update(self, id: int, data: ClubUpdate, current_user: User) -> Club:
        club = await self.club_repo.get_by_id(id)
        if not club:
            raise HTTPException(404, "Club not found")

        if current_user.role.role != "admin":
            membership = await self.membership_repo.get_membership(current_user.id, id)
            if membership is None or not membership.is_leader:
                raise HTTPException(
                    403, "You don't have permission to update this club"
                )

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(club, field, value)
        return await self.club_repo.update(club)

    async def remove_all_members(self,current_user:User,  club_id: int) -> None: 
        club = await self.club_repo.get_by_id(club_id)
        if not club:
            raise HTTPException(404,"Club not found")
        if current_user.role.role != "admin":
            raise HTTPException(
                403, "You don't have permission to update this club"
            )
        members = await self.membership_repo.list_by_club_id(club_id)
        for member in members:
            await self.membership_repo.delete(member)

    async def delete(self,current_user:User, club_id:int)-> None:
        club = await self.club_repo.get_by_id(club_id)
        if not club:
            raise HTTPException(404,"Club not found")
       
        if current_user.role.role != "admin":
            raise HTTPException(
                403,"You have no permission to delete this club"
            )
        members = await self.membership_repo.list_by_club_id(club_id)
        if members:
            raise HTTPException(
                400,
                f"Cannot delete club: {len(members)} still attached. Remove them first"
            )
        return await self.club_repo.delete(club)
