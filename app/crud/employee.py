import base64
from datetime import date, datetime
from decimal import Decimal
from app.supabase_client import get_supabase
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def serialize_employee(employee):
    """Convierte date/datetime a string, Decimal a float y bytes a Base64 para JSON"""
    data = employee.model_dump(exclude_unset=True)

    for key, value in data.items():
        if isinstance(value, (date, datetime)):
            data[key] = value.isoformat()
        elif isinstance(value, bytes):
            data[key] = base64.b64encode(value).decode("utf-8")  
        elif isinstance(value, Decimal):
            data[key] = float(value)  

    return data


async def get_employee(idEmployee: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("employee")
        .select("*")
        .eq("idEmployee", idEmployee)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_employees(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("employee")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_employee(employee: EmployeeCreate):
    supabase = await get_supabase()
    payload = serialize_employee(employee)

    if payload.get("uid"):
        uid_check = (
            await supabase.table("erp_user")
            .select("uid")
            .eq("uid", payload["uid"])
            .single()
            .execute()
        )
        if not uid_check.data:
            raise ValueError("El UID proporcionado no existe en erp_user.")

    result = await supabase.table("employee").insert(payload).execute()
    return result.data[0] if result.data else None


async def update_employee(idEmployee: int, employee: EmployeeUpdate):
    supabase = await get_supabase()
    payload = serialize_employee(employee)

    if "uid" in payload and payload["uid"]:
        uid_check = (
            await supabase.table("erp_user")
            .select("uid")
            .eq("uid", payload["uid"])
            .single()
            .execute()
        )
        if not uid_check.data:
            raise ValueError("El UID proporcionado no existe en erp_user.")

    result = (
        await supabase.table("employee")
        .update(payload)
        .eq("idEmployee", idEmployee)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_employee(idEmployee: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("employee")
        .delete()
        .eq("idEmployee", idEmployee)
        .execute()
    )
    return result.data[0] if result.data else None
