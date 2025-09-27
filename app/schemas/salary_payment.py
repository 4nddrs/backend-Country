from pydantic import BaseModel, Field
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List

# ===== CRUD base =====
class SalaryPaymentBase(BaseModel):
    amount: Decimal
    state: str
    registrationDate: datetime           # timestamp (sin zona)
    paymentDate: Optional[date] = None   # date (opcional)
    fk_idEmployee: int

class SalaryPaymentCreate(SalaryPaymentBase):
    pass  # updateDate lo setea el backend

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


# ===== Reporte / cierre de nómina =====
class SalaryMonthSummaryItem(BaseModel):
    employee_id: int = Field(..., alias="fk_idEmployee")
    employee_name: str
    total_amount: Decimal
    count_payments: int

class SalaryMonthSummaryOut(BaseModel):
    period_month: str            # YYYY-MM
    items: List[SalaryMonthSummaryItem]
    grand_total: Decimal
    total_records: int

class ClosePayrollRequest(BaseModel):
    period_month: str            # YYYY-MM
    create_expense: bool = True
    expense_date: Optional[date] = None        # por defecto hoy
    expense_description: Optional[str] = None  # por defecto "Nómina mes {YYYY-MM}"

class ClosePayrollResult(BaseModel):
    period_month: str
    updated_count: int
    total_amount: Decimal
    expense_id: Optional[int] = None
