from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import nutritional_plan as crud_plan
from app.schemas import nutritional_plan as schemas_plan

router = APIRouter(prefix="/nutritional-plans", tags=["nutritional-plans"])


@router.post(
    "/",
    response_model=schemas_plan.NutritionalPlan,
    status_code=status.HTTP_201_CREATED,
)
async def create_nutritional_plan(plan_in: schemas_plan.NutritionalPlanCreate):
    plan = await crud_plan.create_nutritional_plan(plan_in)
    if not plan:
        raise HTTPException(
            status_code=400, detail="Nutritional plan could not be created"
        )
    return plan


@router.get("/", response_model=List[schemas_plan.NutritionalPlan])
async def list_nutritional_plans(skip: int = 0, limit: int = 100):
    plans = await crud_plan.get_nutritional_plans(skip=skip, limit=limit)
    return plans


@router.get("/{plan_id}", response_model=schemas_plan.NutritionalPlan)
async def get_nutritional_plan(plan_id: int):
    plan = await crud_plan.get_nutritional_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Nutritional plan not found")
    return plan


@router.put("/{plan_id}", response_model=schemas_plan.NutritionalPlan)
async def update_nutritional_plan(
    plan_id: int, plan_in: schemas_plan.NutritionalPlanUpdate
):
    updated_plan = await crud_plan.update_nutritional_plan(plan_id, plan_in)
    if not updated_plan:
        raise HTTPException(status_code=404, detail="Nutritional plan not found")
    return updated_plan


@router.delete("/{plan_id}", response_model=schemas_plan.NutritionalPlan)
async def delete_nutritional_plan(plan_id: int):
    deleted_plan = await crud_plan.delete_nutritional_plan(plan_id)
    if not deleted_plan:
        raise HTTPException(status_code=404, detail="Nutritional plan not found")
    return deleted_plan
