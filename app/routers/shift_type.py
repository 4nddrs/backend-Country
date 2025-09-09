from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import shift_type as crud_shift
from app.schemas import shift_type as schemas_shift

router = APIRouter(prefix="/shift_types", tags=["shift_types"])


@router.post(
    "/", response_model=schemas_shift.ShiftType, status_code=status.HTTP_201_CREATED
)
async def create_shift_type(shift_in: schemas_shift.ShiftTypeCreate):
    shift = await crud_shift.create_shift_type(shift_in)
    if not shift:
        raise HTTPException(status_code=400, detail="Shift type could not be created")
    return shift


@router.get("/", response_model=List[schemas_shift.ShiftType])
async def list_shift_types(skip: int = 0, limit: int = 100):
    shifts = await crud_shift.get_shift_types(skip=skip, limit=limit)
    return shifts


@router.get("/{shift_id}", response_model=schemas_shift.ShiftType)
async def get_shift_type(shift_id: int):
    shift = await crud_shift.get_shift_type(shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift type not found")
    return shift


@router.put("/{shift_id}", response_model=schemas_shift.ShiftType)
async def update_shift_type(shift_id: int, shift_in: schemas_shift.ShiftTypeUpdate):
    updated_shift = await crud_shift.update_shift_type(shift_id, shift_in)
    if not updated_shift:
        raise HTTPException(status_code=404, detail="Shift type not found")
    return updated_shift


@router.delete("/{shift_id}", response_model=schemas_shift.ShiftType)
async def delete_shift_type(shift_id: int):
    deleted_shift = await crud_shift.delete_shift_type(shift_id)
    if not deleted_shift:
        raise HTTPException(status_code=404, detail="Shift type not found")
    return deleted_shift
