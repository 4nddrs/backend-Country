from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import expenses as crud_expenses
from app.schemas import expenses as schemas_expenses

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post(
    "/", response_model=schemas_expenses.Expenses, status_code=status.HTTP_201_CREATED
)
async def create_expense(expense_in: schemas_expenses.ExpensesCreate):
    expense = await crud_expenses.create_expense(expense_in)
    if not expense:
        raise HTTPException(status_code=400, detail="Expense could not be created")
    return expense


@router.get("/", response_model=List[schemas_expenses.Expenses])
async def list_expenses(skip: int = 0, limit: int = 100):
    return await crud_expenses.get_expenses(skip=skip, limit=limit)


@router.get("/{idExpenses}", response_model=schemas_expenses.Expenses)
async def get_expense(idExpenses: int):
    expense = await crud_expenses.get_expense(idExpenses)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{idExpenses}", response_model=schemas_expenses.Expenses)
async def update_expense(idExpenses: int, expense_in: schemas_expenses.ExpensesUpdate):
    updated_expense = await crud_expenses.update_expense(idExpenses, expense_in)
    if not updated_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated_expense


@router.delete("/{idExpenses}", response_model=schemas_expenses.Expenses)
async def delete_expense(idExpenses: int):
    deleted_expense = await crud_expenses.delete_expense(idExpenses)
    if not deleted_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return deleted_expense
