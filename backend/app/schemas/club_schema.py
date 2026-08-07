from pydantic import BaseModel


class ClubCreate(BaseModel):
    name: str
    description: str | None = None


class ClubRead(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True


class ClubUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
