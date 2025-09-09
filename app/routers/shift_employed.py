from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import shift_employed as crud_shift
from app.schemas import shift_employed as schemas_shift

router = APIRouter(prefix="/shift_employeds", tags=["shift_employeds"])


@router.post(
    "/", response_model=schemas_shift.ShiftEmployed, status_code=status.HTTP_201_CREATED
)
async def create_shift_employed(shift_in: schemas_shift.ShiftEmployedCreate):
    shift = await crud_shift.create_shift_employed(shift_in)
    if not shift:
        raise HTTPException(
            status_code=400, detail="ShiftEmployed could not be created"
        )
    return shift


@router.get("/", response_model=List[schemas_shift.ShiftEmployed])
async def list_shift_employeds(skip: int = 0, limit: int = 100):
    shifts = await crud_shift.get_shift_employeds(skip=skip, limit=limit)
    return shifts


@router.get("/{shift_id}", response_model=schemas_shift.ShiftEmployed)
async def get_shift_employed(shift_id: int):
    shift = await crud_shift.get_shift_employed(shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="ShiftEmployed not found")
    return shift


@router.put("/{shift_id}", response_model=schemas_shift.ShiftEmployed)
async def update_shift_employed(
    shift_id: int, shift_in: schemas_shift.ShiftEmployedUpdate
):
    updated_shift = await crud_shift.update_shift_employed(shift_id, shift_in)
    if not updated_shift:
        raise HTTPException(status_code=404, detail="ShiftEmployed not found")
    return updated_shift


@router.delete("/{shift_id}", response_model=schemas_shift.ShiftEmployed)
async def delete_shift_employed(shift_id: int):
    deleted_shift = await crud_shift.delete_shift_employed(shift_id)
    if not deleted_shift:
        raise HTTPException(status_code=404, detail="ShiftEmployed not found")
    return deleted_shift
