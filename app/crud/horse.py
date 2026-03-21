from datetime import date, datetime
from app.supabase_client import get_supabase
from app.schemas.horse import HorseCreate, HorseUpdate


def serialize_horse(horse: dict) -> dict:
    data = horse.copy()
    for key, value in data.items():
        if isinstance(value, (date, datetime)):
            data[key] = value.isoformat()
    return data


async def get_horse(idHorse: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse")
        .select("*")
        .eq("idHorse", idHorse)
        .single()
        .execute()
    )
    return serialize_horse(result.data) if result.data else None


async def get_horses(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [serialize_horse(h) for h in result.data] if result.data else []


async def get_horses_by_owner(idOwner: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse")
        .select("*")
        .eq("fk_idOwner", idOwner)
        .execute()
    )
    return [serialize_horse(h) for h in result.data] if result.data else []


async def create_horse(horse: HorseCreate):
    supabase = await get_supabase()
    result = await supabase.table("horse").insert(horse.model_dump(mode="json")).execute()
    return serialize_horse(result.data[0]) if result.data else None


async def update_horse(idHorse: int, horse: HorseUpdate):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse")
        .update(horse.model_dump(mode="json", exclude_unset=True))
        .eq("idHorse", idHorse)
        .execute()
    )
    return serialize_horse(result.data[0]) if result.data else None


async def update_horse_image(idHorse: int, image_url: str | None):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse")
        .update({"image_url": image_url})
        .eq("idHorse", idHorse)
        .execute()
    )
    return serialize_horse(result.data[0]) if result.data else None


async def delete_horse(idHorse: int):
    supabase = await get_supabase()
    result = await supabase.table("horse").delete().eq("idHorse", idHorse).execute()
    return serialize_horse(result.data[0]) if result.data else None