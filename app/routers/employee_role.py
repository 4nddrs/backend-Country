from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import employee_role as crud_employee_role
from app.schemas import employee_role as schemas_employee_role

router = APIRouter(prefix="/employee_roles", tags=["employee_roles"])

@router.post("/", response_model=schemas_employee_role.EmployeeRole, status_code=status.HTTP_201_CREATED)
async def create_employee_role(role_in: schemas_employee_role.EmployeeRoleCreate):
    role = await crud_employee_role.create_employee_role(role_in)
    if not role:
        raise HTTPException(status_code=400, detail="Could not create employee role")
    return role

@router.get("/", response_model=List[schemas_employee_role.EmployeeRole])
async def list_employee_roles(skip: int = 0, limit: int = 100):
    roles = await crud_employee_role.get_employee_roles(skip=skip, limit=limit)
    return roles

@router.get("/{idRoleEmployee}", response_model=schemas_employee_role.EmployeeRole)
async def get_employee_role(idRoleEmployee: int):
    role = await crud_employee_role.get_employee_role(idRoleEmployee)
    if not role:
        raise HTTPException(status_code=404, detail="Employee role not found")
    return role

@router.put("/{idRoleEmployee}", response_model=schemas_employee_role.EmployeeRole)
async def update_employee_role(
    idRoleEmployee: int,
    role_in: schemas_employee_role.EmployeeRoleUpdate,
):
    updated = await crud_employee_role.update_employee_role(idRoleEmployee, role_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee role not found")
    return updated

@router.delete("/{idRoleEmployee}", response_model=schemas_employee_role.EmployeeRole)
async def delete_employee_role(idRoleEmployee: int):
    deleted = await crud_employee_role.delete_employee_role(idRoleEmployee)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee role not found")
    return deleted
