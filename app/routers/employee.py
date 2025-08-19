from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import employee as crud_employee
from app.schemas import employee as schemas_employee

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=schemas_employee.Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(employee_in: schemas_employee.EmployeeCreate):
    employee = await crud_employee.create_employee(employee_in)
    if not employee:
        raise HTTPException(status_code=400, detail="Could not create employee")
    return employee

@router.get("/", response_model=List[schemas_employee.Employee])
async def list_employees(skip: int = 0, limit: int = 100):
    employees = await crud_employee.get_employees(skip=skip, limit=limit)
    return employees

@router.get("/{idEmployee}", response_model=schemas_employee.Employee)
async def get_employee(idEmployee: int):
    employee = await crud_employee.get_employee(idEmployee)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/{idEmployee}", response_model=schemas_employee.Employee)
async def update_employee(
    idEmployee: int,
    employee_in: schemas_employee.EmployeeUpdate,
):
    updated = await crud_employee.update_employee(idEmployee, employee_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@router.delete("/{idEmployee}", response_model=schemas_employee.Employee)
async def delete_employee(idEmployee: int):
    deleted = await crud_employee.delete_employee(idEmployee)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return deleted
