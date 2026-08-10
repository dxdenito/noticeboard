from pydantic import BaseModel
from datetime import datetime
from app.models.notice import ScopeLevel, Priority, Visibility
from app.schemas.department_schema import DepartmentRead


class NoticeCreate(BaseModel):
    title: str
    body: str
    category_id: int
    scope_level: ScopeLevel
    priority: Priority
    visibility: Visibility
    department_id: int | None = None
    club_id: int | None = None
    course_id: int | None = None
    expiry_date: datetime | None = None


class NoticeRead(BaseModel):
    id: int
    title: str
    body: str
    category_id: int
    author_id: int
    scope_level: ScopeLevel
    priority: Priority
    visibility: Visibility
    department: DepartmentRead | None
    club_id: int | None
    course_id: int | None
    expiry_date: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True
