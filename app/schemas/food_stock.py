from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FoodStockBase(BaseModel):
    foodName: str
    stock: int
    unitMeasurement: float
    unitPrice: float
    fk_idFoodProvider: int


class FoodStockCreate(FoodStockBase):
    pass


class FoodStockUpdate(BaseModel):
    foodName: Optional[str] = None
    stock: Optional[int] = None
    unitMeasurement: Optional[float] = None
    unitPrice: Optional[float] = None
    fk_idFoodProvider: Optional[int] = None


class FoodStockInDBBase(FoodStockBase):
    idFood: int
    created_at: datetime

    class Config:
        orm_mode = True


class FoodStock(FoodStockInDBBase):
    pass
