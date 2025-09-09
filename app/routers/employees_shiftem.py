from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import employees_shiftem as crud_employees
from app.schemas import employees_shiftem as schemas_employees

router = APIRouter(prefix="/employees_shiftems", tags=["employees_shiftems"])


@router.post(
    "/",
    response_model=schemas_employees.EmployeesShiftem,
    status_code=status.HTTP_201_CREATED,
)
async def create_employees_shiftem(
    employees_shiftem_in: schemas_employees.EmployeesShiftemCreate,
):
    emp = await crud_employees.create_employees_shiftem(employees_shiftem_in)
    if not emp:
        raise HTTPException(
            status_code=400, detail="EmployeesShiftem could not be created"
        )
    return emp


@router.get("/", response_model=List[schemas_employees.EmployeesShiftem])
async def list_employees_shiftems(skip: int = 0, limit: int = 100):
    emps = await crud_employees.get_employees_shiftems(skip=skip, limit=limit)
    return emps


@router.get("/{emp_id}", response_model=schemas_employees.EmployeesShiftem)
async def get_employees_shiftem(emp_id: int):
    emp = await crud_employees.get_employees_shiftem(emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="EmployeesShiftem not found")
    return emp


@router.put("/{emp_id}", response_model=schemas_employees.EmployeesShiftem)
async def update_employees_shiftem(
    emp_id: int, employees_shiftem_in: schemas_employees.EmployeesShiftemUpdate
):
    updated_emp = await crud_employees.update_employees_shiftem(
        emp_id, employees_shiftem_in
    )
    if not updated_emp:
        raise HTTPException(status_code=404, detail="EmployeesShiftem not found")
    return updated_emp


@router.delete("/{emp_id}", response_model=schemas_employees.EmployeesShiftem)
async def delete_employees_shiftem(emp_id: int):
    deleted_emp = await crud_employees.delete_employees_shiftem(emp_id)
    if not deleted_emp:
        raise HTTPException(status_code=404, detail="EmployeesShiftem not found")
    return deleted_emp
