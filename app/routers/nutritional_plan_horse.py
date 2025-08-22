from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import nutritional_plan_horse as crud_plan_horse
from app.schemas import nutritional_plan_horse as schemas_plan_horse

router = APIRouter(prefix="/nutritional-plan-horses", tags=["nutritional-plan-horses"])


@router.post(
    "/",
    response_model=schemas_plan_horse.NutritionalPlanHorse,
    status_code=status.HTTP_201_CREATED,
)
async def create_nutritional_plan_horse(
    plan_horse_in: schemas_plan_horse.NutritionalPlanHorseCreate,
):
    plan_horse = await crud_plan_horse.create_nutritional_plan_horse(plan_horse_in)
    if not plan_horse:
        raise HTTPException(
            status_code=400, detail="Nutritional plan assignment could not be created"
        )
    return plan_horse


@router.get("/", response_model=List[schemas_plan_horse.NutritionalPlanHorse])
async def list_nutritional_plan_horses(skip: int = 0, limit: int = 100):
    plans_horses = await crud_plan_horse.get_nutritional_plan_horses(
        skip=skip, limit=limit
    )
    return plans_horses


@router.get("/{plan_horse_id}", response_model=schemas_plan_horse.NutritionalPlanHorse)
async def get_nutritional_plan_horse(plan_horse_id: int):
    plan_horse = await crud_plan_horse.get_nutritional_plan_horse(plan_horse_id)
    if not plan_horse:
        raise HTTPException(
            status_code=404, detail="Nutritional plan assignment not found"
        )
    return plan_horse


@router.put("/{plan_horse_id}", response_model=schemas_plan_horse.NutritionalPlanHorse)
async def update_nutritional_plan_horse(
    plan_horse_id: int, plan_horse_in: schemas_plan_horse.NutritionalPlanHorseUpdate
):
    updated_plan_horse = await crud_plan_horse.update_nutritional_plan_horse(
        plan_horse_id, plan_horse_in
    )
    if not updated_plan_horse:
        raise HTTPException(
            status_code=404, detail="Nutritional plan assignment not found"
        )
    return updated_plan_horse


@router.delete(
    "/{plan_horse_id}", response_model=schemas_plan_horse.NutritionalPlanHorse
)
async def delete_nutritional_plan_horse(plan_horse_id: int):
    deleted_plan_horse = await crud_plan_horse.delete_nutritional_plan_horse(
        plan_horse_id
    )
    if not deleted_plan_horse:
        raise HTTPException(
            status_code=404, detail="Nutritional plan assignment not found"
        )
    return deleted_plan_horse
