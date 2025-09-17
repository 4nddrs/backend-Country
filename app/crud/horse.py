import base64
from datetime import date, datetime
from app.supabase_client import get_supabase
from app.schemas.horse import HorseCreate, HorseUpdate


def serialize_horse(horse: dict):
    """Convierte date/datetime a string y bytes a Base64 para JSON"""
    data = horse.copy()  # evitar mutar directamente el dict original

    for key, value in data.items():
        if isinstance(value, (date, datetime)):
            data[key] = value.isoformat()
        elif isinstance(value, bytes):
            data[key] = base64.b64encode(value).decode("utf-8")

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


async def create_horse(horse: HorseCreate):
    supabase = await get_supabase()
    horse_dict = horse.model_dump(mode="json")

    # ⚡ NO decodificamos la foto, ya viene en Base64 y JSON lo acepta
    # if horse_dict.get("horsePhoto"):
    #     horse_dict["horsePhoto"] = base64.b64decode(horse_dict["horsePhoto"])

    result = await supabase.table("horse").insert(horse_dict).execute()
    return serialize_horse(result.data[0]) if result.data else None


async def update_horse(idHorse: int, horse: HorseUpdate):
    supabase = await get_supabase()
    horse_dict = horse.model_dump(mode="json", exclude_unset=True)

    # ⚡ NO decodificamos la foto
    # if horse_dict.get("horsePhoto"):
    #     horse_dict["horsePhoto"] = base64.b64decode(horse_dict["horsePhoto"])

    result = (
        await supabase.table("horse")
        .update(horse_dict)
        .eq("idHorse", idHorse)
        .execute()
    )
    return serialize_horse(result.data[0]) if result.data else None


async def delete_horse(idHorse: int):
    supabase = await get_supabase()
    result = await supabase.table("horse").delete().eq("idHorse", idHorse).execute()
    return serialize_horse(result.data[0]) if result.data else None
