from pydantic import BaseModel
from datetime import datetime, date


class ExpensesBase(BaseModel):
    date: date
    description: str
    AmountBsCaptureType: float
    period: date


class ExpensesCreate(ExpensesBase):
    pass


class ExpensesUpdate(ExpensesBase):
    pass


class ExpensesInDBBase(ExpensesBase):
    idExpenses: int
    created_at: datetime

    class Config:
        from_attributes = True


class Expenses(ExpensesInDBBase):
    pass
