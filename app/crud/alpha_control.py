from datetime import date
from decimal import Decimal
from app.supabase_client import get_supabase
from app.schemas.alpha_control import AlphaControlCreate, AlphaControlUpdate


def serialize_alpha_control(record: dict):
    """Convierte campos especiales (date, decimal → float)."""
    if record.get("date") and isinstance(record["date"], date):
        record["date"] = record["date"].isoformat()

    for field in [
        "alphaIncome",
        "unitPrice",
        "totalPurchasePrice",
        "outcome",
        "balance",
        "salePrice",
        "income",
    ]:
        if record.get(field) is not None:
            record[field] = float(record[field])

    return record


async def get_alpha_control(idAlphaControl: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("alpha_control")
        .select("*")
        .eq("idAlphaControl", idAlphaControl)
        .single()
        .execute()
    )
    return serialize_alpha_control(result.data) if result.data else None


async def get_alpha_controls(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("alpha_control")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [serialize_alpha_control(r) for r in result.data] if result.data else []


async def create_alpha_control(alpha_control: AlphaControlCreate):
    supabase = await get_supabase()
    data = alpha_control.model_dump(mode="json")
    result = await supabase.table("alpha_control").insert(data).execute()
    return serialize_alpha_control(result.data[0]) if result.data else None


async def update_alpha_control(idAlphaControl: int, alpha_control: AlphaControlUpdate):
    supabase = await get_supabase()
    data = alpha_control.model_dump(mode="json", exclude_unset=True)
    result = (
        await supabase.table("alpha_control")
        .update(data)
        .eq("idAlphaControl", idAlphaControl)
        .execute()
    )
    return serialize_alpha_control(result.data[0]) if result.data else None


async def delete_alpha_control(idAlphaControl: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("alpha_control")
        .delete()
        .eq("idAlphaControl", idAlphaControl)
        .execute()
    )
    return serialize_alpha_control(result.data[0]) if result.data else None
