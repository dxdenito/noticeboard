from pydantic import BaseModel, EmailStr
from app.schemas.role_schema import RoleRead


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    department_id: int | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: RoleRead
    department_id: int | None
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRoleUpdate(BaseModel):
    role_id: int
