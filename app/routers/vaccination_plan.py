from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import vaccination_plan as crud_plan
from app.schemas import vaccination_plan as schemas_plan

router = APIRouter(prefix="/vaccination_plan", tags=["vaccination_plan"])


@router.post(
    "/",
    response_model=schemas_plan.VaccinationPlan,
    status_code=status.HTTP_201_CREATED,
)
async def create_vaccination_plan(plan_in: schemas_plan.VaccinationPlanCreate):
    plan = await crud_plan.create_vaccination_plan(plan_in)
    if not plan:
        raise HTTPException(
            status_code=400, detail="VaccinationPlan could not be created"
        )
    return plan


@router.get("/", response_model=List[schemas_plan.VaccinationPlan])
async def list_vaccination_plans(skip: int = 0, limit: int = 100):
    return await crud_plan.get_vaccination_plans(skip=skip, limit=limit)


@router.get("/{idVaccinationPlan}", response_model=schemas_plan.VaccinationPlan)
async def get_vaccination_plan(idVaccinationPlan: int):
    plan = await crud_plan.get_vaccination_plan(idVaccinationPlan)
    if not plan:
        raise HTTPException(status_code=404, detail="VaccinationPlan not found")
    return plan


@router.put("/{idVaccinationPlan}", response_model=schemas_plan.VaccinationPlan)
async def update_vaccination_plan(
    idVaccinationPlan: int, plan_in: schemas_plan.VaccinationPlanUpdate
):
    updated_plan = await crud_plan.update_vaccination_plan(idVaccinationPlan, plan_in)
    if not updated_plan:
        raise HTTPException(status_code=404, detail="VaccinationPlan not found")
    return updated_plan


@router.delete("/{idVaccinationPlan}", response_model=schemas_plan.VaccinationPlan)
async def delete_vaccination_plan(idVaccinationPlan: int):
    deleted_plan = await crud_plan.delete_vaccination_plan(idVaccinationPlan)
    if not deleted_plan:
        raise HTTPException(status_code=404, detail="VaccinationPlan not found")
    return deleted_plan
