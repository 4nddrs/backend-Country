from fastapi import APIRouter, HTTPException, status
from typing import List

from app.crud import salary_payment as crud_salary
from app.schemas import salary_payment as schemas_salary

router = APIRouter(prefix="/salary_payments", tags=["salary_payments"])


@router.post("/", response_model=schemas_salary.SalaryPayment, status_code=status.HTTP_201_CREATED)
async def create_salary_payment(salary_in: schemas_salary.SalaryPaymentCreate):
    created = await crud_salary.create_salary_payment(salary_in)
    if not created:
        raise HTTPException(status_code=400, detail="Salary payment could not be created")
    return created


@router.get("/", response_model=List[schemas_salary.SalaryPayment])
async def list_salary_payments(skip: int = 0, limit: int = 100):
    rows = await crud_salary.get_salary_payments(skip=skip, limit=limit)
    return rows


@router.get("/{salary_id}", response_model=schemas_salary.SalaryPayment)
async def get_salary_payment(salary_id: int):
    row = await crud_salary.get_salary_payment(salary_id)
    if not row:
        raise HTTPException(status_code=404, detail="Salary payment not found")
    return row


@router.put("/{salary_id}", response_model=schemas_salary.SalaryPayment)
async def update_salary_payment(salary_id: int, salary_in: schemas_salary.SalaryPaymentUpdate):
    updated = await crud_salary.update_salary_payment(salary_id, salary_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Salary payment not found")
    return updated


@router.delete("/{salary_id}", response_model=schemas_salary.SalaryPayment)
async def delete_salary_payment(salary_id: int):
    deleted = await crud_salary.delete_salary_payment(salary_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Salary payment not found")
    return deleted
