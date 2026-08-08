from pydantic import BaseModel


class CourseEnrollmentCreate(BaseModel):
    user_id: int


class CourseEnrollmentRead(BaseModel):
    user_id: int
    course_id: int
    is_leader: bool

    class Config:
        from_attributes = True


class CourseLeaderUpdate(BaseModel):
    is_leader: bool
