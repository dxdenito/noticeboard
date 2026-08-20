from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.club_schema import (
    ClubCreate,
    ClubRead,
    ClubUpdate,
)
from app.schemas.club_membership_schema import (
    ClubMembershipCreate,
    ClubMembershipRead,
    ClubLeaderUpdate,
)
from app.core.deps import get_current_user, require_roles, get_db
from app.services.club_service import ClubService
from app.services.club_membership_service import ClubMembershipService
from app.models.user import User

router = APIRouter(prefix="/clubs", tags=["clubs"])


@router.post("/", response_model=ClubRead)
async def create_club(
    data: ClubCreate,
    current_user: User = Depends(require_roles("admin")),
    db=Depends(get_db),
):
    club_service = ClubService(db)
    new_club = await club_service.create(data)
    return new_club


@router.get("/", response_model=list[ClubRead])
async def list_clubs(db=Depends(get_db)):  # no auth dependency at all — public
    club_service = ClubService(db)
    return await club_service.list_all()


@router.get("/{id}", response_model=ClubRead)
async def get_club(id: int, db=Depends(get_db)):  # public
    club_service = ClubService(db)
    return await club_service.get_by_id(id)


@router.put("/{id}", response_model=ClubRead)
async def update_club(
    id: int,
    data: ClubUpdate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):

    club_service = ClubService(db)
    new_club = await club_service.update(id, data, current_user)
    return new_club


@router.post("/{club_id}/members", response_model=ClubMembershipRead)
async def add_club_member(
    club_id: int,
    data: ClubMembershipCreate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    membership_service = ClubMembershipService(db)
    return await membership_service.add_member(club_id, data.user_id, current_user)


@router.patch("/{club_id}/members/{user_id}/leader", response_model=ClubMembershipRead)
async def set_club_leader(
    club_id: int,
    user_id: int,
    data: ClubLeaderUpdate,
    current_user: User = Depends(require_roles("admin")),
    db=Depends(get_db),
):
    membership_service = ClubMembershipService(db)
    return await membership_service.set_leader(
        club_id, user_id, data.is_leader, current_user
    )

@router.patch("/{id}/remove-all-members")
async def remove_all_club_members(
    id: int,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    club_service = ClubService(db)
    await club_service.remove_all_members(current_user, id)
    return {"message": "All members removed"}


@router.delete("/{id}", status_code=204)
async def delete_club(
    id: int,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    club_service = ClubService(db)
    await club_service.delete(current_user, id)
