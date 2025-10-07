from __future__ import annotations
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from typing import Optional, Union


class AlphaControlBase(BaseModel):
    date: date   # coincide con la columna en la tabla
    alphaIncome: float
    unitPrice: float
    totalPurchasePrice: float
    outcome: float
    balance: float
    salePrice: float
    income: float
    fk_idFoodProvider: Optional[int] = None


class AlphaControlCreate(AlphaControlBase):
    pass


class AlphaControlUpdate(BaseModel):
    date: Optional[Union[date, str]] = None
    alphaIncome: Optional[float] = None
    unitPrice: Optional[float] = None
    totalPurchasePrice: Optional[float] = None
    outcome: Optional[float] = None
    balance: Optional[float] = None
    salePrice: Optional[float] = None
    income: Optional[float] = None
    fk_idFoodProvider: Optional[int] = None


class AlphaControlInDBBase(AlphaControlBase):
    idAlphaControl: int
    created_at: datetime

    class Config:
        from_attributes = True


class AlphaControl(AlphaControlInDBBase):
    provider: Optional[dict] = None
