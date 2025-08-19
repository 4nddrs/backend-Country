from app.supabase_client import get_supabase
from app.schemas.employee_role import EmployeeRoleCreate, EmployeeRoleUpdate

async def get_employee_role(idRoleEmployee: int):
    supabase = await get_supabase()
    result = await supabase.table("employee_role").select("*").eq("idRoleEmployee", idRoleEmployee).single().execute()
    return result.data if result.data else None

async def get_employee_roles(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = await supabase.table("employee_role").select("*").range(skip, skip + limit - 1).execute()
    return result.data if result.data else []

async def create_employee_role(role: EmployeeRoleCreate):
    supabase = await get_supabase()
    result = await supabase.table("employee_role").insert(role.model_dump()).execute()
    return result.data[0] if result.data else None

async def update_employee_role(idRoleEmployee: int, role: EmployeeRoleUpdate):
    supabase = await get_supabase()
    result = await supabase.table("employee_role").update(role.model_dump(exclude_unset=True)).eq("idRoleEmployee", idRoleEmployee).execute()
    return result.data[0] if result.data else None

async def delete_employee_role(idRoleEmployee: int):
    supabase = await get_supabase()
    result = await supabase.table("employee_role").delete().eq("idRoleEmployee", idRoleEmployee).execute()
    return result.data[0] if result.data else None
