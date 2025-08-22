from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import vaccine as crud_vaccine
from app.schemas import vaccine as schemas_vaccine

router = APIRouter(prefix="/vaccines", tags=["vaccines"])


@router.post(
    "/", response_model=schemas_vaccine.Vaccine, status_code=status.HTTP_201_CREATED
)
async def create_vaccine(vaccine_in: schemas_vaccine.VaccineCreate):
    vaccine = await crud_vaccine.create_vaccine(vaccine_in)
    if not vaccine:
        raise HTTPException(status_code=400, detail="Vaccine could not be created")
    return vaccine


@router.get("/", response_model=List[schemas_vaccine.Vaccine])
async def list_vaccines(skip: int = 0, limit: int = 100):
    vaccines = await crud_vaccine.get_vaccines(skip=skip, limit=limit)
    return vaccines


@router.get("/{vaccine_id}", response_model=schemas_vaccine.Vaccine)
async def get_vaccine(vaccine_id: int):
    vaccine = await crud_vaccine.get_vaccine(vaccine_id)
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return vaccine


@router.put("/{vaccine_id}", response_model=schemas_vaccine.Vaccine)
async def update_vaccine(vaccine_id: int, vaccine_in: schemas_vaccine.VaccineUpdate):
    updated_vaccine = await crud_vaccine.update_vaccine(vaccine_id, vaccine_in)
    if not updated_vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return updated_vaccine


@router.delete("/{vaccine_id}", response_model=schemas_vaccine.Vaccine)
async def delete_vaccine(vaccine_id: int):
    deleted_vaccine = await crud_vaccine.delete_vaccine(vaccine_id)
    if not deleted_vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return deleted_vaccine
