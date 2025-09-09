from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import food_stock as crud_food_stock
from app.schemas import food_stock as schemas_food_stock

router = APIRouter(prefix="/food-stock", tags=["food_stock"])


@router.post(
    "/",
    response_model=schemas_food_stock.FoodStock,
    status_code=status.HTTP_201_CREATED,
)
async def create_food_stock(food_stock_in: schemas_food_stock.FoodStockCreate):
    food_stock = await crud_food_stock.create_food_stock(food_stock_in)
    if not food_stock:
        raise HTTPException(status_code=400, detail="Food stock could not be created")
    return food_stock


@router.get("/", response_model=List[schemas_food_stock.FoodStock])
async def list_food_stocks(skip: int = 0, limit: int = 100):
    return await crud_food_stock.get_food_stocks(skip=skip, limit=limit)


@router.get("/{food_id}", response_model=schemas_food_stock.FoodStock)
async def get_food_stock(food_id: int):
    food_stock = await crud_food_stock.get_food_stock(food_id)
    if not food_stock:
        raise HTTPException(status_code=404, detail="Food stock not found")
    return food_stock


@router.put("/{food_id}", response_model=schemas_food_stock.FoodStock)
async def update_food_stock(
    food_id: int, food_stock_in: schemas_food_stock.FoodStockUpdate
):
    updated = await crud_food_stock.update_food_stock(food_id, food_stock_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Food stock not found")
    return updated


@router.delete("/{food_id}", response_model=schemas_food_stock.FoodStock)
async def delete_food_stock(food_id: int):
    deleted = await crud_food_stock.delete_food_stock(food_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Food stock not found")
    return deleted
