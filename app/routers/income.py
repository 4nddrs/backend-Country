from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import income as crud_income
from app.schemas import income as schemas_income

router = APIRouter(prefix="/income", tags=["income"])


@router.post(
    "/", response_model=schemas_income.Income, status_code=status.HTTP_201_CREATED
)
async def create_income(income_in: schemas_income.IncomeCreate):
    income = await crud_income.create_income(income_in)
    if not income:
        raise HTTPException(status_code=400, detail="Income could not be created")
    return income


@router.get("/", response_model=List[schemas_income.Income])
async def list_incomes(skip: int = 0, limit: int = 100):
    return await crud_income.get_incomes(skip=skip, limit=limit)


@router.get("/{idIncome}", response_model=schemas_income.Income)
async def get_income(idIncome: int):
    income = await crud_income.get_income(idIncome)
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    return income


@router.put("/{idIncome}", response_model=schemas_income.Income)
async def update_income(idIncome: int, income_in: schemas_income.IncomeUpdate):
    updated_income = await crud_income.update_income(idIncome, income_in)
    if not updated_income:
        raise HTTPException(status_code=404, detail="Income not found")
    return updated_income


@router.delete("/{idIncome}", response_model=schemas_income.Income)
async def delete_income(idIncome: int):
    deleted_income = await crud_income.delete_income(idIncome)
    if not deleted_income:
        raise HTTPException(status_code=404, detail="Income not found")
    return deleted_income
