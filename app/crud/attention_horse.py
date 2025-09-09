from datetime import date
from app.supabase_client import get_supabase
from app.schemas.attention_horse import AttentionHorseCreate, AttentionHorseUpdate


def serialize_attention_horse(attention: dict):
    """Convierte campos especiales (date → isoformat)."""
    if attention.get("date") and isinstance(attention["date"], date):
        attention["date"] = attention["date"].isoformat()
    return attention


async def get_attention_horse(idAttentionHorse: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("attention_horse")
        .select("*")
        .eq("idAttentionHorse", idAttentionHorse)
        .single()
        .execute()
    )
    return serialize_attention_horse(result.data) if result.data else None


async def get_attention_horses(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("attention_horse")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [serialize_attention_horse(a) for a in result.data] if result.data else []


async def create_attention_horse(attention: AttentionHorseCreate):
    supabase = await get_supabase()
    attention_dict = attention.model_dump(mode="json")
    result = await supabase.table("attention_horse").insert(attention_dict).execute()
    return serialize_attention_horse(result.data[0]) if result.data else None


async def update_attention_horse(
    idAttentionHorse: int, attention: AttentionHorseUpdate
):
    supabase = await get_supabase()
    attention_dict = attention.model_dump(mode="json", exclude_unset=True)
    result = (
        await supabase.table("attention_horse")
        .update(attention_dict)
        .eq("idAttentionHorse", idAttentionHorse)
        .execute()
    )
    return serialize_attention_horse(result.data[0]) if result.data else None


async def delete_attention_horse(idAttentionHorse: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("attention_horse")
        .delete()
        .eq("idAttentionHorse", idAttentionHorse)
        .execute()
    )
    return serialize_attention_horse(result.data[0]) if result.data else None
