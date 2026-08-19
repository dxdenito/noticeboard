from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.repositories.department_repository import DepartmentRepository
from app.models.department import Department
from app.models.user import User
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate
from app.repositories.course_repository import CourseRepository
from app.repositories.user_repository import UserRepository


class DepartmentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.dept_repo = DepartmentRepository(db)
        self.course_repo = CourseRepository(db)
        self.user_repo = UserRepository(db)

    async def create(self, data: DepartmentCreate) -> Department:
        new_department = Department(**data.model_dump())
        try:
            return await self.dept_repo.create(new_department)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A department with this name or code already exists",
            )

    async def list_all(self) -> list[Department]:
        return await self.dept_repo.list_all()

    async def get_by_id(self, id: int) -> Department:
        department = await self.dept_repo.get_by_id(id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
            )
        return department

    async def update(
        self, id: int, data: DepartmentUpdate, current_user: User
    ) -> Department:
        department = await self.dept_repo.get_by_id(id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
            )

        if current_user.role.role == "hod" and current_user.department_id != id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this department",
            )

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(department, field, value)

        try:
            return await self.dept_repo.update(department)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A department with this name or code already exists",
            )

    async def reassign_children(
        self, from_department_id: int, to_department_id: int
    ) -> dict:
        from_dept = await self.dept_repo.get_by_id(from_department_id)
        if not from_dept:
            raise HTTPException(404, "Source department not found")

        to_dept = await self.dept_repo.get_by_id(to_department_id)
        if not to_dept:
            raise HTTPException(404, "Target department not found")

        if from_department_id == to_department_id:
            raise HTTPException(400, "Source and target department cannot be the same")

        courses = await self.course_repo.list_by_department_id(from_department_id)
        for course in courses:
            course.department_id = to_department_id
            await self.course_repo.update(course)

        users = await self.user_repo.list_by_department_id(from_department_id)
        for user in users:
            user.department_id = to_department_id
            await self.user_repo.update(user)

        return {"courses_moved": len(courses), "users_moved": len(users)}

    async def delete(self, department_id: int) -> None:
        department = await self.dept_repo.get_by_id(department_id)
        if not department:
            raise HTTPException(404, "Department not found")

        courses = await self.course_repo.list_by_department_id(department_id)
        users = await self.user_repo.list_by_department_id(department_id)

        if courses or users:
            raise HTTPException(
                400,
                f"Cannot delete: {len(courses)} course(s) and {len(users)} user(s) still assigned. Reassign them first.",
            )

        await self.dept_repo.delete(department)
