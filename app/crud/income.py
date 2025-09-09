from datetime import date, datetime
from app.supabase_client import get_supabase
from app.schemas.income import IncomeCreate, IncomeUpdate


def serialize_income(income):
    """Convierte date/datetime a string para JSON"""
    data = income.model_dump(exclude_unset=True)
    for key, value in data.items():
        if isinstance(value, (date, datetime)):
            data[key] = value.isoformat()
    return data


async def get_income(idIncome: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("income")
        .select("*")
        .eq("idIncome", idIncome)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_incomes(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("income")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_income(income: IncomeCreate):
    supabase = await get_supabase()
    payload = serialize_income(income)
    result = await supabase.table("income").insert(payload).execute()
    return result.data[0] if result.data else None


async def update_income(idIncome: int, income: IncomeUpdate):
    supabase = await get_supabase()
    payload = serialize_income(income)
    result = (
        await supabase.table("income")
        .update(payload)
        .eq("idIncome", idIncome)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_income(idIncome: int):
    supabase = await get_supabase()
    result = await supabase.table("income").delete().eq("idIncome", idIncome).execute()
    return result.data[0] if result.data else None
