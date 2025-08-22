from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import horse as crud_horse
from app.schemas import horse as schemas_horse

router = APIRouter(prefix="/horses", tags=["horses"])


@router.post(
    "/", response_model=schemas_horse.Horse, status_code=status.HTTP_201_CREATED
)
async def create_horse(horse_in: schemas_horse.HorseCreate):
    horse = await crud_horse.create_horse(horse_in)
    if not horse:
        raise HTTPException(status_code=400, detail="Horse could not be created")
    return horse


@router.get("/", response_model=List[schemas_horse.Horse])
async def list_horses(skip: int = 0, limit: int = 100):
    horses = await crud_horse.get_horses(skip=skip, limit=limit)
    return horses


@router.get("/{horse_id}", response_model=schemas_horse.Horse)
async def get_horse(horse_id: int):
    horse = await crud_horse.get_horse(horse_id)
    if not horse:
        raise HTTPException(status_code=404, detail="Horse not found")
    return horse


@router.put("/{horse_id}", response_model=schemas_horse.Horse)
async def update_horse(horse_id: int, horse_in: schemas_horse.HorseUpdate):
    updated_horse = await crud_horse.update_horse(horse_id, horse_in)
    if not updated_horse:
        raise HTTPException(status_code=404, detail="Horse not found")
    return updated_horse


@router.delete("/{horse_id}", response_model=schemas_horse.Horse)
async def delete_horse(horse_id: int):
    deleted_horse = await crud_horse.delete_horse(horse_id)
    if not deleted_horse:
        raise HTTPException(status_code=404, detail="Horse not found")
    return deleted_horse
