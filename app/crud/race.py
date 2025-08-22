from app.supabase_client import get_supabase
from app.schemas.race import RaceCreate, RaceUpdate


async def get_race(race_id: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("race")
        .select("*")
        .eq("idRace", race_id)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_races(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("race").select("*").range(skip, skip + limit - 1).execute()
    )
    return result.data if result.data else []


async def create_race(race: RaceCreate):
    supabase = await get_supabase()
    result = await supabase.table("race").insert(race.model_dump()).execute()
    return result.data[0] if result.data else None


async def update_race(race_id: int, race: RaceUpdate):
    supabase = await get_supabase()
    result = (
        await supabase.table("race")
        .update(race.model_dump(exclude_unset=True))
        .eq("idRace", race_id)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_race(race_id: int):
    supabase = await get_supabase()
    result = await supabase.table("race").delete().eq("idRace", race_id).execute()
    return result.data[0] if result.data else None
