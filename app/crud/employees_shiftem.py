from app.supabase_client import get_supabase
from app.schemas.employees_shiftem import EmployeesShiftemCreate, EmployeesShiftemUpdate


async def get_employees_shiftem(idEmployeesShiftem: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("employees_shiftem")
        .select("*")
        .eq("idEmployeesShiftem", idEmployeesShiftem)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_employees_shiftems(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("employees_shiftem")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_employees_shiftem(employees_shiftem: EmployeesShiftemCreate):
    supabase = await get_supabase()
    data_dict = employees_shiftem.model_dump(mode="json")
    result = await supabase.table("employees_shiftem").insert(data_dict).execute()
    return result.data[0] if result.data else None


async def update_employees_shiftem(
    idEmployeesShiftem: int, employees_shiftem: EmployeesShiftemUpdate
):
    supabase = await get_supabase()
    data_dict = employees_shiftem.model_dump(mode="json", exclude_unset=True)
    result = (
        await supabase.table("employees_shiftem")
        .update(data_dict)
        .eq("idEmployeesShiftem", idEmployeesShiftem)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_employees_shiftem(idEmployeesShiftem: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("employees_shiftem")
        .delete()
        .eq("idEmployeesShiftem", idEmployeesShiftem)
        .execute()
    )
    return result.data[0] if result.data else None
