from app.supabase_client import get_supabase
from app.schemas.shift_type import ShiftTypeCreate, ShiftTypeUpdate


async def get_shift_type(idShiftType: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("shift_type")
        .select("*")
        .eq("idShiftType", idShiftType)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_shift_types(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("shift_type")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_shift_type(shift: ShiftTypeCreate):
    supabase = await get_supabase()
    shift_dict = shift.model_dump(mode="json")
    result = await supabase.table("shift_type").insert(shift_dict).execute()
    return result.data[0] if result.data else None


async def update_shift_type(idShiftType: int, shift: ShiftTypeUpdate):
    supabase = await get_supabase()
    shift_dict = shift.model_dump(mode="json", exclude_unset=True)
    result = (
        await supabase.table("shift_type")
        .update(shift_dict)
        .eq("idShiftType", idShiftType)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_shift_type(idShiftType: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("shift_type")
        .delete()
        .eq("idShiftType", idShiftType)
        .execute()
    )
    return result.data[0] if result.data else None
