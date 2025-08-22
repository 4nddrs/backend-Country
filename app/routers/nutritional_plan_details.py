from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import nutritional_plan_details as crud_details
from app.schemas import nutritional_plan_details as schemas_details

router = APIRouter(
    prefix="/nutritional-plan-details", tags=["nutritional-plan-details"]
)


@router.post(
    "/",
    response_model=schemas_details.NutritionalPlanDetails,
    status_code=status.HTTP_201_CREATED,
)
async def create_nutritional_plan_detail(
    detail_in: schemas_details.NutritionalPlanDetailsCreate,
):
    detail = await crud_details.create_nutritional_plan_detail(detail_in)
    if not detail:
        raise HTTPException(
            status_code=400, detail="Nutritional plan detail could not be created"
        )
    return detail


@router.get("/", response_model=List[schemas_details.NutritionalPlanDetails])
async def list_nutritional_plan_details(skip: int = 0, limit: int = 100):
    details = await crud_details.get_nutritional_plan_details(skip=skip, limit=limit)
    return details


@router.get("/{detail_id}", response_model=schemas_details.NutritionalPlanDetails)
async def get_nutritional_plan_detail(detail_id: int):
    detail = await crud_details.get_nutritional_plan_detail(detail_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Nutritional plan detail not found")
    return detail


@router.put("/{detail_id}", response_model=schemas_details.NutritionalPlanDetails)
async def update_nutritional_plan_detail(
    detail_id: int, detail_in: schemas_details.NutritionalPlanDetailsUpdate
):
    updated_detail = await crud_details.update_nutritional_plan_detail(
        detail_id, detail_in
    )
    if not updated_detail:
        raise HTTPException(status_code=404, detail="Nutritional plan detail not found")
    return updated_detail


@router.delete("/{detail_id}", response_model=schemas_details.NutritionalPlanDetails)
async def delete_nutritional_plan_detail(detail_id: int):
    deleted_detail = await crud_details.delete_nutritional_plan_detail(detail_id)
    if not deleted_detail:
        raise HTTPException(status_code=404, detail="Nutritional plan detail not found")
    return deleted_detail
