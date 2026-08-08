from pydantic import BaseModel

class ClubMembershipCreate(BaseModel):
    user_id: int

class ClubMembershipRead(BaseModel):
    user_id: int
    club_id: int
    is_leader: bool

    class Config:
        from_attributes = True

class ClubLeaderUpdate(BaseModel):
    is_leader: bool