from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    department_id: int | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role_id: int
    department_id: int | None
    is_active: bool

    class Config:
        from_attributes = (
            True  # lets this schema build directly from a SQLAlchemy User object
        )


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRoleUpdate(BaseModel):
    role_id: int
