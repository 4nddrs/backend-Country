from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FoodStockBase(BaseModel):
    foodName: str
    stock: int
    unitMeasurement: float
    minStock: int
    maxStock: int
    fk_idFoodProvider: int


class FoodStockCreate(FoodStockBase):
    pass


class FoodStockUpdate(BaseModel):
    foodName: Optional[str] = None
    stock: Optional[int] = None
    unitMeasurement: Optional[float] = None
    minStock: Optional[int] = None
    maxStock: Optional[int] = None
    fk_idFoodProvider: Optional[int] = None


class FoodStockInDBBase(FoodStockBase):
    idFood: int
    created_at: datetime

    class Config:
        from_attributes = True


class FoodStock(FoodStockInDBBase):
    pass
