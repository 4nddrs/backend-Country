from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.crud import salary_payment as crud
from app.schemas import salary_payment as schemas

router = APIRouter(prefix="/salary-payment", tags=["salary_payment"])

# ===== CRUD =====
@router.post("/", response_model=schemas.SalaryPayment, status_code=status.HTTP_201_CREATED)
async def create_salary_payment(payload: schemas.SalaryPaymentCreate):
    created = await crud.create_salary_payment(payload)
    if not created:
        raise HTTPException(status_code=400, detail="Salary payment could not be created")
    return created

@router.get("/", response_model=List[schemas.SalaryPayment])
async def list_salary_payments(skip: int = 0, limit: int = 100):
    return await crud.get_salary_payments(skip=skip, limit=limit)

@router.get("/{salary_payment_id}", response_model=schemas.SalaryPayment)
async def get_salary_payment(salary_payment_id: int):
    sp = await crud.get_salary_payment(salary_payment_id)
    if not sp:
        raise HTTPException(status_code=404, detail="Salary payment not found")
    return sp

@router.put("/{salary_payment_id}", response_model=schemas.SalaryPayment)
async def update_salary_payment(salary_payment_id: int, payload: schemas.SalaryPaymentUpdate):
    updated = await crud.update_salary_payment(salary_payment_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Salary payment not found")
    return updated

@router.delete("/{salary_payment_id}", response_model=schemas.SalaryPayment)
async def delete_salary_payment(salary_payment_id: int):
    deleted = await crud.delete_salary_payment(salary_payment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Salary payment not found")
    return deleted

# ===== Reporte / Cierre =====
@router.get("/payroll/summary", response_model=schemas.SalaryMonthSummaryOut)
async def payroll_summary(period_month: str = Query(..., example="2025-09")):
    try:
        return await crud.salary_month_summary(period_month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/payroll/close", response_model=schemas.ClosePayrollResult)
async def payroll_close(payload: schemas.ClosePayrollRequest):
    try:
        return await crud.close_month_payroll(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
