from datetime import date, datetime
from app.supabase_client import get_supabase
from app.schemas.expenses import ExpensesCreate, ExpensesUpdate


def serialize_expense(expense):
    """Convierte date/datetime a string para JSON"""
    data = expense.model_dump(exclude_unset=True)
    for key, value in data.items():
        if isinstance(value, (date, datetime)):
            data[key] = value.isoformat()
    return data


async def get_expense(idExpenses: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("expenses")
        .select("*")
        .eq("idExpenses", idExpenses)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_expenses(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("expenses")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_expense(expense: ExpensesCreate):
    supabase = await get_supabase()
    payload = serialize_expense(expense)
    result = await supabase.table("expenses").insert(payload).execute()
    return result.data[0] if result.data else None


async def update_expense(idExpenses: int, expense: ExpensesUpdate):
    supabase = await get_supabase()
    payload = serialize_expense(expense)
    result = (
        await supabase.table("expenses")
        .update(payload)
        .eq("idExpenses", idExpenses)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_expense(idExpenses: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("expenses").delete().eq("idExpenses", idExpenses).execute()
    )
    return result.data[0] if result.data else None
