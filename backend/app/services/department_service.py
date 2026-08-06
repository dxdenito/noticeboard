from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.repositories.department_repository import DepartmentRepository
from app.models.department import Department
from app.models.user import User
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate


class DepartmentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.dept_repo = DepartmentRepository(db)

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
        return department

    async def update(self, id: int, data: DepartmentUpdate, current_user: User) -> Department:
        department = await self.dept_repo.get_by_id(id)
        if not department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

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