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

# ====== SalaryPayment ======
class SalaryPaymentBase(BaseModel):
    amount: Decimal = Field(..., gt=0)
    state: str
    # <-- ahora opcional; el backend/BD la setean si no llega
    registrationDate: Optional[datetime] = None
    paymentDate: Optional[date] = None
    fk_idEmployee: int

class SalaryPaymentCreate(SalaryPaymentBase):
    # sin cambios: al heredar, registrationDate ya es opcional
    pass

class SalaryPaymentUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    state: Optional[str] = None
    registrationDate: Optional[datetime] = None
    paymentDate: Optional[date] = None
    fk_idEmployee: Optional[int] = None

class SalaryPaymentInDBBase(SalaryPaymentBase):
    idSalaryPayment: int
    created_at: datetime
    updateDate: datetime

    class Config:
        from_attributes = True

class SalaryPayment(SalaryPaymentInDBBase):
    # empleado embebido para el front
    employee: Optional[EmployeeLite] = None

# ====== Listado paginado ======
class SalaryPaymentList(BaseModel):
    items: List[SalaryPayment]
    total: int
    page: int
    limit: int

# ====== Resumen mensual / cierre ======
class MonthSummary(BaseModel):
    month: str          # "YYYY-MM"
    totalAmount: Decimal
    count: int

class CloseMonthResponse(MonthSummary):
    expenseCreated: bool
    expenseId: Optional[int] = None
