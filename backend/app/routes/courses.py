from fastapi import APIRouter, Depends
from app.schemas.course_schema import (
    CourseCreate,
    CourseRead,
    CourseUpdate,
)
from app.core.deps import get_current_user, require_roles, get_db
from app.services.course_service import CourseService
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.course_enrollment_service import CourseEnrollmentService


from app.schemas.course_enrollment_schema import (
    CourseEnrollmentCreate,
    CourseEnrollmentRead,
    CourseLeaderUpdate,
)
from app.services.course_enrollment_service import CourseEnrollmentService

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


@router.post("/{course_id}/members", response_model=CourseEnrollmentRead)
async def add_course_member(
    course_id: int,
    data: CourseEnrollmentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    enrollment_service = CourseEnrollmentService(db)
    return await enrollment_service.add_enrollment(
        course_id, data.user_id, current_user
    )


@router.patch(
    "/{course_id}/members/{user_id}/leader", response_model=CourseEnrollmentRead
)
async def set_course_leader(
    course_id: int,
    user_id: int,
    data: CourseLeaderUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    enrollment_service = CourseEnrollmentService(db)
    return await enrollment_service.set_leader(
        course_id, user_id, data.is_leader, current_user
    )


@router.patch("/{id}/remove-all-enrollments")
async def remove_all_course_enrollments(
    id: int,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    course_service = CourseService(db)
    await course_service.remove_all_enrollments(current_user, id)
    return {"message": "All enrollments removed"}


@router.delete("/{id}", status_code=204)
async def delete_course(
    id: int,
    current_user: User = Depends(require_roles("admin")),
    db: AsyncSession = Depends(get_db),
):
    course_service = CourseService(db)
    await course_service.delete(current_user, id)
