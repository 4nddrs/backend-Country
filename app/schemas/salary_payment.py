# app/schemas/salary_payment.py
from pydantic import BaseModel, Field
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List

# ========== Empleado (para combos / embedding) ==========
class EmployeeLite(BaseModel):
    idEmployee: int
    fullName: str
    ci: int
    positionName: Optional[str] = None
    salary: Decimal

# ========== SalaryPayment ==========
class SalaryPaymentBase(BaseModel):
    amount: Decimal = Field(..., gt=0)
    state: str
    paymentDate: Optional[date] = None
    fk_idEmployee: int

# CREATE: el front NO envía registrationDate
class SalaryPaymentCreate(SalaryPaymentBase):
    pass

# UPDATE: todo opcional
class SalaryPaymentUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    state: Optional[str] = None
    registrationDate: Optional[datetime] = None
    paymentDate: Optional[date] = None
    fk_idEmployee: Optional[int] = None

class SalaryPaymentInDBBase(BaseModel):
    idSalaryPayment: int
    created_at: datetime
    registrationDate: datetime
    updateDate: datetime
    amount: Decimal
    state: str
    paymentDate: Optional[date] = None
    fk_idEmployee: int

    class Config:
        from_attributes = True

class SalaryPayment(SalaryPaymentInDBBase):
    employee: Optional[EmployeeLite] = None

# Listado paginado
class SalaryPaymentList(BaseModel):
    items: List[SalaryPayment]
    total: int
    page: int
    limit: int
