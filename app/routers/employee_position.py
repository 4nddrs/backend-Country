from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import employee_position as crud_employee_position
from app.schemas import employee_position as schemas_employee_position

router = APIRouter(prefix="/employee_positions", tags=["employee_positions"])

@router.post("/", response_model=schemas_employee_position.EmployeePosition, status_code=status.HTTP_201_CREATED)
async def create_employee_position(position_in: schemas_employee_position.EmployeePositionCreate):
    position = await crud_employee_position.create_employee_position(position_in)
    if not position:
        raise HTTPException(status_code=400, detail="Could not create employee position")
    return position

@router.get("/", response_model=List[schemas_employee_position.EmployeePosition])
async def list_employee_positions(skip: int = 0, limit: int = 100):
    positions = await crud_employee_position.get_employee_positions(skip=skip, limit=limit)
    return positions

@router.get("/{idPositionEmployee}", response_model=schemas_employee_position.EmployeePosition)
async def get_employee_position(idPositionEmployee: int):
    position = await crud_employee_position.get_employee_position(idPositionEmployee)
    if not position:
        raise HTTPException(status_code=404, detail="Employee position not found")
    return position

@router.put("/{idPositionEmployee}", response_model=schemas_employee_position.EmployeePosition)
async def update_employee_position(
    idPositionEmployee: int,
    position_in: schemas_employee_position.EmployeePositionUpdate,
):
    updated = await crud_employee_position.update_employee_position(idPositionEmployee, position_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee position not found")
    return updated

@router.delete("/{idPositionEmployee}", response_model=schemas_employee_position.EmployeePosition)
async def delete_employee_position(idPositionEmployee: int):
    deleted = await crud_employee_position.delete_employee_position(idPositionEmployee)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee position not found")
    return deleted
