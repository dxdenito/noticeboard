from pydantic import BaseModel

class RoleRead(BaseModel):
    id: int
    role: str

    class Config:
        from_attributes = True