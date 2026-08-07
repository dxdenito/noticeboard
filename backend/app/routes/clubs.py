from fastapi import APIRouter, Depends
from app.schemas.club_schema import (
    ClubCreate,
    ClubRead,
    ClubUpdate,
)
from app.core.deps import get_current_user, require_roles, get_db
from app.services.club_service import ClubService
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
