from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
from typing import Optional


# ====== Relación con empleado ======
class PositionEmployee(BaseModel):
    idPositionEmployee: int
    namePosition: str

    class Config:
        from_attributes = True


class EmployeeLite(BaseModel):
    idEmployee: int
    fullName: str
    employee_position: Optional[PositionEmployee] = None

    class Config:
        from_attributes = True


# ====== Tip Payment ======
class TipPaymentBase(BaseModel):
    amount: Decimal
    state: str
    description: str               # 👈 nuevo campo obligatorio
    paymentDate: Optional[date] = None
    fk_idEmployee: int


class TipPaymentCreate(TipPaymentBase):
    """El cliente NO manda registrationDate, lo genera el backend"""
    pass


class TipPaymentUpdate(BaseModel):
    amount: Optional[Decimal] = None
    state: Optional[str] = None
    description: Optional[str] = None   # 👈 editable
    paymentDate: Optional[date] = None
    fk_idEmployee: Optional[int] = None
    updateDate: Optional[datetime] = None


class TipPaymentInDBBase(TipPaymentBase):
    idTipPayment: int
    created_at: datetime
    registrationDate: datetime
    updateDate: datetime

    class Config:
        from_attributes = True


class TipPayment(TipPaymentInDBBase):
    employee: Optional[EmployeeLite] = None
