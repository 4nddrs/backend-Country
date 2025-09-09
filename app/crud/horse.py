import base64
from datetime import date
from app.supabase_client import get_supabase
from app.schemas.horse import HorseCreate, HorseUpdate

def serialize_horse(horse: dict):
    """Convierte campos especiales (date, bytes → Base64)."""
    if horse.get("birthdate") and isinstance(horse["birthdate"], date):
        horse["birthdate"] = horse["birthdate"].isoformat()

    if horse.get("horsePhoto") and isinstance(horse["horsePhoto"], (bytes, bytearray)):
        horse["horsePhoto"] = base64.b64encode(horse["horsePhoto"]).decode("utf-8")

    return horse

async def get_horse(idHorse: int):
    supabase = await get_supabase()
    result = await supabase.table("horse").select("*").eq("idHorse", idHorse).single().execute()
    return serialize_horse(result.data) if result.data else None

async def get_horses(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = await supabase.table("horse").select("*").range(skip, skip + limit - 1).execute()
    return [serialize_horse(h) for h in result.data] if result.data else []

async def create_horse(horse: HorseCreate):
    supabase = await get_supabase()
    horse_dict = horse.model_dump(mode="json")

    # Foto en Base64 → bytes
    if horse_dict.get("horsePhoto"):
        horse_dict["horsePhoto"] = base64.b64decode(horse_dict["horsePhoto"])

    result = await supabase.table("horse").insert(horse_dict).execute()
    return serialize_horse(result.data[0]) if result.data else None

async def update_horse(idHorse: int, horse: HorseUpdate):
    supabase = await get_supabase()
    horse_dict = horse.model_dump(mode="json", exclude_unset=True)

    if horse_dict.get("horsePhoto"):
        horse_dict["horsePhoto"] = base64.b64decode(horse_dict["horsePhoto"])

    result = await supabase.table("horse").update(horse_dict).eq("idHorse", idHorse).execute()
    return serialize_horse(result.data[0]) if result.data else None

async def delete_horse(idHorse: int):
    supabase = await get_supabase()
    result = await supabase.table("horse").delete().eq("idHorse", idHorse).execute()
    return serialize_horse(result.data[0]) if result.data else None
