from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
from typing import Optional


class SalaryPaymentBase(BaseModel):
    amount: Decimal
    state: str
    registrationDate: datetime
    paymentDate: Optional[date] = None
    fk_idEmployee: int


class SalaryPaymentCreate(SalaryPaymentBase):
    pass


class SalaryPaymentUpdate(BaseModel):
    amount: Optional[Decimal] = None
    state: Optional[str] = None
    registrationDate: Optional[datetime] = None
    paymentDate: Optional[date] = None
    fk_idEmployee: Optional[int] = None
    updateDate: Optional[datetime] = None


class SalaryPaymentInDBBase(SalaryPaymentBase):
    idSalaryPayment: int
    created_at: datetime
    updateDate: datetime

    class Config:
        from_attributes = True


class SalaryPayment(SalaryPaymentInDBBase):
    pass
