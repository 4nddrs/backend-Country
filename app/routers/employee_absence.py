from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import employee_absence as crud_absence
from app.schemas import employee_absence as schemas_absence

router = APIRouter(prefix="/employee_absences", tags=["employee_absences"])


@router.post(
    "/",
    response_model=schemas_absence.EmployeeAbsence,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee_absence(absence_in: schemas_absence.EmployeeAbsenceCreate):
    absence = await crud_absence.create_employee_absence(absence_in)
    if not absence:
        raise HTTPException(
            status_code=400, detail="Employee absence could not be created"
        )
    return absence


@router.get("/", response_model=List[schemas_absence.EmployeeAbsence])
async def list_employee_absences(skip: int = 0, limit: int = 100):
    absences = await crud_absence.get_employee_absences(skip=skip, limit=limit)
    return absences


@router.get("/{absence_id}", response_model=schemas_absence.EmployeeAbsence)
async def get_employee_absence(absence_id: int):
    absence = await crud_absence.get_employee_absence(absence_id)
    if not absence:
        raise HTTPException(status_code=404, detail="Employee absence not found")
    return absence


@router.put("/{absence_id}", response_model=schemas_absence.EmployeeAbsence)
async def update_employee_absence(
    absence_id: int, absence_in: schemas_absence.EmployeeAbsenceUpdate
):
    updated_absence = await crud_absence.update_employee_absence(absence_id, absence_in)
    if not updated_absence:
        raise HTTPException(status_code=404, detail="Employee absence not found")
    return updated_absence


@router.delete("/{absence_id}", response_model=schemas_absence.EmployeeAbsence)
async def delete_employee_absence(absence_id: int):
    deleted_absence = await crud_absence.delete_employee_absence(absence_id)
    if not deleted_absence:
        raise HTTPException(status_code=404, detail="Employee absence not found")
    return deleted_absence
