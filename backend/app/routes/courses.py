from fastapi import APIRouter, Depends
from app.schemas.course_schema import (
    CourseCreate,
    CourseRead,
    CourseUpdate,
)
from app.core.deps import get_current_user, require_roles, get_db
from app.services.course_service import CourseService
from app.models.user import User

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=CourseRead)
async def create_course(
    data: CourseCreate,
    current_user: User = Depends(require_roles("admin")),
    db=Depends(get_db),
):
    course_service = CourseService(db)
    new_course = await course_service.create(data)
    return new_course


@router.get("/", response_model=list[CourseRead])
async def list_courses(db=Depends(get_db)):  # no auth dependency at all — public
    course_service = CourseService(db)
    return await course_service.list_all()


@router.get("/{id}", response_model=CourseRead)
async def get_course(id: int, db=Depends(get_db)):  # public
    course_service = CourseService(db)
    return await course_service.get_by_id(id)


@router.put("/{id}", response_model=CourseRead)
async def update_course(
    id: int,
    data: CourseUpdate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    
    course_service = CourseService(db)
    new_course = await course_service.update(id, data, current_user)
    return new_course
