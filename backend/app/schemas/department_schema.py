from pydantic import BaseModel

class DepartmentCreate(BaseModel):
    name: str
    code: str

class DepartmentRead(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True

class DepartmentUpdate(BaseModel):
    name: str | None = None
    code: str | None = None