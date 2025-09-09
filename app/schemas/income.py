from pydantic import BaseModel
from datetime import datetime, date


class IncomeBase(BaseModel):
    date: date
    description: str
    amountBsCaptureType: float
    period: date


class IncomeCreate(IncomeBase):
    pass


class IncomeUpdate(IncomeBase):
    pass


class IncomeInDBBase(IncomeBase):
    idIncome: int
    created_at: datetime

    class Config:
        from_attributes = True


class Income(IncomeInDBBase):
    pass
