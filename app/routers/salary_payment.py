# app/routers/salary_payments.py
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from app.crud import salary_payment as crud_salary
from app.schemas.salary_payment import (
    SalaryPayment, SalaryPaymentCreate, SalaryPaymentUpdate,
    SalaryPaymentList, EmployeeLite
)

router = APIRouter(prefix="/salary-payments", tags=["salary-payments"])

# -------- Empleados (para combos) --------
@router.get("/employees", response_model=List[EmployeeLite])
async def list_employees_for_form(
    search: Optional[str] = None,
    limit: int = Query(50, ge=1, le=5000),
):
    return await crud_salary.list_employees_for_payment(search=search, limit=limit)

# ====================== CRUD ======================

# Create (acepta /salary-payments y /salary-payments/)
@router.post("", response_model=SalaryPayment, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=SalaryPayment, status_code=status.HTTP_201_CREATED)
async def create_salary_payment(salary_in: SalaryPaymentCreate):
    sp = await crud_salary.create_salary_payment(salary_in)
    if not sp:
        raise HTTPException(status_code=400, detail="Salary payment could not be created")
    return sp

# List (acepta con/sin barra final)
@router.get("", response_model=SalaryPaymentList)
@router.get("/", response_model=SalaryPaymentList)
async def list_salary_payments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=200),
    employeeId: Optional[int] = None,
    state: Optional[str] = None,
    month: Optional[str] = None,              # YYYY-MM (sobre registrationDate)
    orderBy: str = "registrationDate",
    order: str = "desc",
):
    return await crud_salary.list_salary_payments(
        page=page,
        limit=limit,
        employeeId=employeeId,
        state=state,
        month=month,
        orderBy=orderBy,
        order=order,
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
