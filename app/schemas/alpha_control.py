from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class AlphaControlBase(BaseModel):
    date: date
    alphaIncome: float
    unitPrice: float
    totalPurchasePrice: float
    outcome: float
    balance: float
    salePrice: float
    income: float
    closingAmount: str
    fk_idFoodProvider: int


class AlphaControlCreate(AlphaControlBase):
    pass


class AlphaControlUpdate(AlphaControlBase):
    pass


class AlphaControlInDBBase(AlphaControlBase):
    idAlphaControl: int
    created_at: datetime

    class Config:
        from_attributes = True


class AlphaControl(AlphaControlInDBBase):
    pass
