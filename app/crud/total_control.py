from datetime import datetime
from app.supabase_client import get_supabase
from app.schemas.total_control import TotalControlCreate, TotalControlUpdate


def serialize_total_control(control):
    """Convierte datetime a string para JSON"""
    data = control.model_dump(exclude_unset=True)
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    return data


async def get_total_control(idTotalControl: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("total_control")
        .select("*")
        .eq("idTotalControl", idTotalControl)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_total_controls(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("total_control")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_total_control(control: TotalControlCreate):
    supabase = await get_supabase()
    payload = serialize_total_control(control)
    result = await supabase.table("total_control").insert(payload).execute()
    return result.data[0] if result.data else None


async def update_total_control(idTotalControl: int, control: TotalControlUpdate):
    supabase = await get_supabase()
    payload = serialize_total_control(control)
    result = (
        await supabase.table("total_control")
        .update(payload)
        .eq("idTotalControl", idTotalControl)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_total_control(idTotalControl: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("total_control")
        .delete()
        .eq("idTotalControl", idTotalControl)
        .execute()
    )
    return result.data[0] if result.data else None
