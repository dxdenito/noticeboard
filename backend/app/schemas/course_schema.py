from pydantic import BaseModel

class CourseCreate(BaseModel):
    name: str
    code: str
    department_id: int

class CourseRead(BaseModel):
    id: int
    name: str
    code: str
    department_id: int

    class Config:
        from_attributes = True

class CourseUpdate(BaseModel):
    name: str | None = None
    code: str | None = None