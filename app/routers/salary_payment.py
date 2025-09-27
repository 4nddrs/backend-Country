from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from datetime import date

from app.crud import salary_payment as crud_salary
from app.schemas.salary_payment import (
    SalaryPayment, SalaryPaymentCreate, SalaryPaymentUpdate,
    SalaryPaymentList, MonthSummary, CloseMonthResponse, EmployeeLite
)

router = APIRouter(prefix="/salary-payments", tags=["salary-payments"])

# -------- Autocomplete Empleados --------
@router.get("/employees", response_model=List[EmployeeLite])
async def list_employees_for_form(search: Optional[str] = None, limit: int = 20):
    return await crud_salary.list_employees_for_payment(search=search, limit=limit)

# -------- Resumen mensual --------
@router.get("/summary/month", response_model=MonthSummary)
async def salary_month_summary(
    month: str = Query(..., description="Formato YYYY-MM"),
    state: Optional[str] = "PAID",
    employeeId: Optional[int] = None,
    usePaymentDate: bool = True,
):
    total, count = await crud_salary.month_summary_total(
        month=month, state=state, employeeId=employeeId, usePaymentDate=usePaymentDate
    )
    return {"month": month, "totalAmount": total, "count": count}

# -------- Cierre de mes -> expenses --------
@router.post("/close-month", response_model=CloseMonthResponse)
async def close_month_create_expense(
    month: str = Query(..., description="Formato YYYY-MM"),
    description: Optional[str] = Query(None),
    expenseDate: Optional[date] = Query(None),
    state: Optional[str] = "PAID",
    employeeId: Optional[int] = None,
    usePaymentDate: bool = True,
):
    total, count = await crud_salary.month_summary_total(
        month=month, state=state, employeeId=employeeId, usePaymentDate=usePaymentDate
    )
    if total <= 0:
        return {
            "month": month,
            "totalAmount": total,
            "count": count,
            "expenseCreated": False,
            "expenseId": None
        }

    exp_id = await crud_salary.create_expense_from_month_total(
        month=month, total=total, description=description, expenseDate=expenseDate
    )
    return {
        "month": month,
        "totalAmount": total,
        "count": count,
        "expenseCreated": True,
        "expenseId": exp_id
    }

# ====================== CRUD ======================
@router.post("/", response_model=SalaryPayment, status_code=status.HTTP_201_CREATED)
async def create_salary_payment(salary_in: SalaryPaymentCreate):
    sp = await crud_salary.create_salary_payment(salary_in)
    if not sp:
        raise HTTPException(status_code=400, detail="Salary payment could not be created")
    return sp

@router.get("/", response_model=SalaryPaymentList)
async def list_salary_payments(
    page: int = 1,
    limit: int = 10,
    employeeId: Optional[int] = None,
    state: Optional[str] = None,
    month: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    search: Optional[str] = None,
    orderBy: str = "registrationDate",
    order: str = "desc",
):
    return await crud_salary.list_salary_payments(
        page=page, limit=limit, employeeId=employeeId, state=state,
        month=month, date_from=date_from, date_to=date_to, search=search,
        orderBy=orderBy, order=order
    )

@router.get("/{salary_id}", response_model=SalaryPayment)
async def get_salary_payment(salary_id: int):
    sp = await crud_salary.get_salary_payment(salary_id)
    if not sp:
        raise HTTPException(status_code=404, detail="Salary payment not found")
    return sp

@router.put("/{salary_id}", response_model=SalaryPayment)
async def update_salary_payment(salary_id: int, salary_in: SalaryPaymentUpdate):
    sp = await crud_salary.update_salary_payment(salary_id, salary_in)
    if not sp:
        raise HTTPException(status_code=404, detail="Salary payment not found")
    return sp

@router.delete("/{salary_id}", response_model=SalaryPayment)
async def delete_salary_payment(salary_id: int):
    sp = await crud_salary.delete_salary_payment(salary_id)
    if not sp:
        raise HTTPException(status_code=404, detail="Salary payment not found")
    return sp
