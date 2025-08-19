# app/crud/employee_position.py
from app.supabase_client import get_supabase
from app.schemas.employee_position import EmployeePositionCreate, EmployeePositionUpdate

async def get_employee_position(idPositionEmployee: int):
    supabase = await get_supabase()
    result = await supabase.table("employee_position").select("*").eq("idPositionEmployee", idPositionEmployee).single().execute()
    return result.data if result.data else None

async def get_employee_positions(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = await supabase.table("employee_position").select("*").range(skip, skip + limit - 1).execute()
    return result.data if result.data else []

async def create_employee_position(position: EmployeePositionCreate):
    supabase = await get_supabase()
    result = await supabase.table("employee_position").insert(position.model_dump()).execute()
    return result.data[0] if result.data else None

async def update_employee_position(idPositionEmployee: int, position: EmployeePositionUpdate):
    supabase = await get_supabase()
    result = await supabase.table("employee_position").update(position.model_dump(exclude_unset=True)).eq("idPositionEmployee", idPositionEmployee).execute()
    return result.data[0] if result.data else None

async def delete_employee_position(idPositionEmployee: int):
    supabase = await get_supabase()
    result = await supabase.table("employee_position").delete().eq("idPositionEmployee", idPositionEmployee).execute()
    return result.data[0] if result.data else None
