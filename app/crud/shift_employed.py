from datetime import datetime
from app.supabase_client import get_supabase
from app.schemas.shift_employed import ShiftEmployedCreate, ShiftEmployedUpdate


def serialize_shift_employed(shift: dict):
    """Convierte campos datetime a ISO string."""
    for field in ["startDateTime", "endDateTime"]:
        if shift.get(field) and isinstance(shift[field], datetime):
            shift[field] = shift[field].isoformat()
    return shift


async def get_shift_employed(idShiftEmployed: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("shift_employed")
        .select("*")
        .eq("idShiftEmployed", idShiftEmployed)
        .single()
        .execute()
    )
    return serialize_shift_employed(result.data) if result.data else None


async def get_shift_employeds(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("shift_employed")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [serialize_shift_employed(s) for s in result.data] if result.data else []


async def create_shift_employed(shift: ShiftEmployedCreate):
    supabase = await get_supabase()
    shift_dict = shift.model_dump(mode="json")
    result = await supabase.table("shift_employed").insert(shift_dict).execute()
    return serialize_shift_employed(result.data[0]) if result.data else None


async def update_shift_employed(idShiftEmployed: int, shift: ShiftEmployedUpdate):
    supabase = await get_supabase()
    shift_dict = shift.model_dump(mode="json", exclude_unset=True)
    result = (
        await supabase.table("shift_employed")
        .update(shift_dict)
        .eq("idShiftEmployed", idShiftEmployed)
        .execute()
    )
    return serialize_shift_employed(result.data[0]) if result.data else None


async def delete_shift_employed(idShiftEmployed: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("shift_employed")
        .delete()
        .eq("idShiftEmployed", idShiftEmployed)
        .execute()
    )
    return serialize_shift_employed(result.data[0]) if result.data else None
