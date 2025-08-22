from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import food_provider as crud_food_provider
from app.schemas import food_provider as schemas_food_provider

router = APIRouter(prefix="/food-providers", tags=["food_providers"])


@router.post(
    "/",
    response_model=schemas_food_provider.FoodProvider,
    status_code=status.HTTP_201_CREATED,
)
async def create_food_provider(
    food_provider_in: schemas_food_provider.FoodProviderCreate,
):
    food_provider = await crud_food_provider.create_food_provider(food_provider_in)
    if not food_provider:
        raise HTTPException(
            status_code=400, detail="Food provider could not be created"
        )
    return food_provider


@router.get("/", response_model=List[schemas_food_provider.FoodProvider])
async def list_food_providers(skip: int = 0, limit: int = 100):
    return await crud_food_provider.get_food_providers(skip=skip, limit=limit)


@router.get("/{food_provider_id}", response_model=schemas_food_provider.FoodProvider)
async def get_food_provider(food_provider_id: int):
    food_provider = await crud_food_provider.get_food_provider(food_provider_id)
    if not food_provider:
        raise HTTPException(status_code=404, detail="Food provider not found")
    return food_provider


@router.put("/{food_provider_id}", response_model=schemas_food_provider.FoodProvider)
async def update_food_provider(
    food_provider_id: int, food_provider_in: schemas_food_provider.FoodProviderUpdate
):
    updated = await crud_food_provider.update_food_provider(
        food_provider_id, food_provider_in
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Food provider not found")
    return updated


@router.delete("/{food_provider_id}", response_model=schemas_food_provider.FoodProvider)
async def delete_food_provider(food_provider_id: int):
    deleted = await crud_food_provider.delete_food_provider(food_provider_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Food provider not found")
    return deleted
