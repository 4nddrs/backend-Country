from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import medicine as crud_medicine
from app.schemas import medicine as schemas_medicine

router = APIRouter(prefix="/medicines", tags=["medicines"])


@router.post(
    "/", response_model=schemas_medicine.Medicine, status_code=status.HTTP_201_CREATED
)
async def create_medicine(medicine_in: schemas_medicine.MedicineCreate):
    medicine = await crud_medicine.create_medicine(medicine_in)
    if not medicine:
        raise HTTPException(status_code=400, detail="Medicine could not be created")
    return medicine


@router.get("/", response_model=List[schemas_medicine.Medicine])
async def list_medicines(skip: int = 0, limit: int = 100):
    medicines = await crud_medicine.get_medicines(skip=skip, limit=limit)
    return medicines


@router.get("/{medicine_id}", response_model=schemas_medicine.Medicine)
async def get_medicine(medicine_id: int):
    medicine = await crud_medicine.get_medicine(medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


@router.put("/{medicine_id}", response_model=schemas_medicine.Medicine)
async def update_medicine(
    medicine_id: int, medicine_in: schemas_medicine.MedicineUpdate
):
    updated_medicine = await crud_medicine.update_medicine(medicine_id, medicine_in)
    if not updated_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return updated_medicine


@router.delete("/{medicine_id}", response_model=schemas_medicine.Medicine)
async def delete_medicine(medicine_id: int):
    deleted_medicine = await crud_medicine.delete_medicine(medicine_id)
    if not deleted_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return deleted_medicine
