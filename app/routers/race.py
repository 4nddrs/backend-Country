from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import race as crud_race
from app.schemas import race as schemas_race

router = APIRouter(prefix="/race", tags=["race"])


@router.post("/", response_model=schemas_race.Race, status_code=status.HTTP_201_CREATED)
async def create_race(race_in: schemas_race.RaceCreate):
    race = await crud_race.create_race(race_in)
    if not race:
        raise HTTPException(status_code=400, detail="Race could not be created")
    return race


@router.get("/", response_model=List[schemas_race.Race])
async def list_races(skip: int = 0, limit: int = 100):
    races = await crud_race.get_races(skip=skip, limit=limit)
    return races


@router.get("/{race_id}", response_model=schemas_race.Race)
async def get_race(race_id: int):
    race = await crud_race.get_race(race_id)
    if not race:
        raise HTTPException(status_code=404, detail="Race not found")
    return race


@router.put("/{race_id}", response_model=schemas_race.Race)
async def update_race(race_id: int, race_in: schemas_race.RaceUpdate):
    updated_race = await crud_race.update_race(race_id, race_in)
    if not updated_race:
        raise HTTPException(status_code=404, detail="Race not found")
    return updated_race


@router.delete("/{race_id}", response_model=schemas_race.Race)
async def delete_race(race_id: int):
    deleted_race = await crud_race.delete_race(race_id)
    if not deleted_race:
        raise HTTPException(status_code=404, detail="Race not found")
    return deleted_race
