from fastapi import APIRouter, Depends
from app.schemas.department_schema import (
    DepartmentCreate,
    DepartmentRead,
    DepartmentUpdate,
)
from app.core.deps import get_current_user, require_roles, get_db
from app.services.department_service import DepartmentService
from app.models.user import User

router = APIRouter(prefix="/departments", tags=["departments"])


@router.post("/", response_model=DepartmentRead)
async def create_department(
    data: DepartmentCreate,
    current_user: User = Depends(require_roles("admin")),
    db=Depends(get_db),
): 
    department_service = DepartmentService(db)
    new_department = await department_service.create(data)
    return new_department



@router.get("/", response_model=list[DepartmentRead])
async def list_departments(db=Depends(get_db)):  # no auth dependency at all — public
    department_service = DepartmentService(db)
    return await department_service.list_all()


@router.get("/{id}", response_model=DepartmentRead)
async def get_department(id: int, db=Depends(get_db)):  # public
    department_service = DepartmentService(db)
    return await department_service.get_by_id(id)


@router.put("/{id}", response_model=DepartmentRead)
async def update_department(
    id: int,
    data: DepartmentUpdate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    # note: NOT require_roles here — both admin and hod are allowed, and the "only their own dept" check needs the service's finer-grained logic
    department_service = DepartmentService(db)
    new_department = await department_service.update(id, data, current_user)
    return new_department
