from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import vaccination_plan_application as crud_app
from app.schemas import vaccination_plan_application as schemas_app

router = APIRouter(
    prefix="/vaccination_plan_application", tags=["vaccination_plan_application"]
)


@router.post(
    "/",
    response_model=schemas_app.VaccinationPlanApplication,
    status_code=status.HTTP_201_CREATED,
)
async def create_vaccination_plan_application(
    plan_app_in: schemas_app.VaccinationPlanApplicationCreate,
):
    plan_app = await crud_app.create_vaccination_plan_application(plan_app_in)
    if not plan_app:
        raise HTTPException(
            status_code=400, detail="VaccinationPlanApplication could not be created"
        )
    return plan_app


@router.get("/", response_model=List[schemas_app.VaccinationPlanApplication])
async def list_vaccination_plan_applications(skip: int = 0, limit: int = 100):
    return await crud_app.get_vaccination_plan_applications(skip=skip, limit=limit)


@router.get(
    "/{idVaccinationPlanApplication}",
    response_model=schemas_app.VaccinationPlanApplication,
)
async def get_vaccination_plan_application(idVaccinationPlanApplication: int):
    plan_app = await crud_app.get_vaccination_plan_application(
        idVaccinationPlanApplication
    )
    if not plan_app:
        raise HTTPException(
            status_code=404, detail="VaccinationPlanApplication not found"
        )
    return plan_app


@router.put(
    "/{idVaccinationPlanApplication}",
    response_model=schemas_app.VaccinationPlanApplication,
)
async def update_vaccination_plan_application(
    idVaccinationPlanApplication: int,
    plan_app_in: schemas_app.VaccinationPlanApplicationUpdate,
):
    updated_plan_app = await crud_app.update_vaccination_plan_application(
        idVaccinationPlanApplication, plan_app_in
    )
    if not updated_plan_app:
        raise HTTPException(
            status_code=404, detail="VaccinationPlanApplication not found"
        )
    return updated_plan_app


@router.delete(
    "/{idVaccinationPlanApplication}",
    response_model=schemas_app.VaccinationPlanApplication,
)
async def delete_vaccination_plan_application(idVaccinationPlanApplication: int):
    deleted_plan_app = await crud_app.delete_vaccination_plan_application(
        idVaccinationPlanApplication
    )
    if not deleted_plan_app:
        raise HTTPException(
            status_code=404, detail="VaccinationPlanApplication not found"
        )
    return deleted_plan_app
