# app/schemas/salary_payment.py
from pydantic import BaseModel, Field
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List

# ====== Empleado (para autocompletar / respuesta) ======
class EmployeeLite(BaseModel):
    idEmployee: int
    fullName: str
    ci: int
    positionName: Optional[str] = None
    salary: Decimal

# ====== CREATE / UPDATE ======
class SalaryPaymentCreate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    state: str
    paymentDate: Optional[date] = None
    fk_idEmployee: int
    # 👈 NO incluimos registrationDate aquí

class SalaryPaymentUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    state: Optional[str] = None
    registrationDate: Optional[datetime] = None   # se puede editar si quisieras
    paymentDate: Optional[date] = None
    fk_idEmployee: Optional[int] = None

# ====== MODELOS DE RESPUESTA ======
class SalaryPaymentInDBBase(BaseModel):
    idSalaryPayment: int
    created_at: datetime
    amount: Decimal
    state: str
    registrationDate: datetime
    paymentDate: Optional[date] = None
    updateDate: datetime
    fk_idEmployee: int

    class Config:
        from_attributes = True

class SalaryPayment(SalaryPaymentInDBBase):
    employee: Optional[EmployeeLite] = None

class SalaryPaymentList(BaseModel):
    items: List[SalaryPayment]
    total: int
    page: int
    limit: int

class MonthSummary(BaseModel):
    month: str
    totalAmount: Decimal
    count: int

class CloseMonthResponse(MonthSummary):
    expenseCreated: bool
    expenseId: Optional[int] = None
