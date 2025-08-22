from app.supabase_client import get_supabase
from app.schemas.horse import HorseCreate, HorseUpdate


async def get_horse(horse_id: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse")
        .select("*")
        .eq("idHorse", horse_id)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_horses(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_horse(horse: HorseCreate):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse").insert(horse.model_dump(mode="json")).execute()
    )
    return result.data[0] if result.data else None


async def update_horse(horse_id: int, horse: HorseUpdate):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse")
        .update(horse.model_dump(mode="json", exclude_unset=True))
        .eq("idHorse", horse_id)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_horse(horse_id: int):
    supabase = await get_supabase()
    result = await supabase.table("horse").delete().eq("idHorse", horse_id).execute()
    return result.data[0] if result.data else None
