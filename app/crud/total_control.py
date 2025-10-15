from datetime import datetime, date
from app.supabase_client import get_supabase
from app.schemas.total_control import TotalControlCreate, TotalControlUpdate


def serialize_total_control(control):
    if not control:
        return {}

    data = control.model_dump(exclude_unset=True)

    for key, value in list(data.items()):
        if isinstance(value, (datetime, date)):
            data[key] = value.isoformat()
        elif value is None:
            data.pop(key)

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
        .order("idTotalControl", desc=True)
        .execute()
    )
    return result.data or []


async def create_total_control(control: TotalControlCreate):
    supabase = await get_supabase()
    payload = serialize_total_control(control)
    result = await supabase.table("total_control").insert(payload).execute()
    return result.data[0] if result.data else None


async def update_total_control(idTotalControl: int, control: TotalControlUpdate):
    supabase = await get_supabase()
    payload = serialize_total_control(control)
    if not payload:
        return None
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
