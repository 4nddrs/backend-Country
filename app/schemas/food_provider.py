from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FoodProviderBase(BaseModel):
    supplierName: str
    cellphoneNumber: int
    generalDescription: Optional[str] = None


class FoodProviderCreate(FoodProviderBase):
    pass


class FoodProviderUpdate(BaseModel):
    supplierName: Optional[str] = None
    cellphoneNumber: Optional[int] = None
    generalDescription: Optional[str] = None


class FoodProviderInDBBase(FoodProviderBase):
    idFoodProvider: int
    created_at: datetime

    class Config:
        orm_mode = True


class FoodProvider(FoodProviderInDBBase):
    pass
