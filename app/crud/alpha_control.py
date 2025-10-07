from datetime import date
from decimal import Decimal
from app.supabase_client import get_supabase
from app.schemas.alpha_control import AlphaControlCreate, AlphaControlUpdate


def serialize_alpha_control(record: dict):
    """Convierte campos especiales (date, decimal → float) y normaliza proveedor."""
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
        if record.get(field) is not None and isinstance(record[field], (Decimal, float, int)):
            record[field] = float(record[field])

    if "food_provider" in record and record["food_provider"]:
        record["provider"] = {
            "idFoodProvider": record["food_provider"].get("idFoodProvider"),
            "supplierName": record["food_provider"].get("supplierName"),
        }
        del record["food_provider"]

    return record



async def get_alpha_control(idAlphaControl: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("alpha_control")
        .select("*, food_provider(idFoodProvider, supplierName)")
        .eq("idAlphaControl", idAlphaControl)
        .single()
        .execute()
    )
    return serialize_alpha_control(result.data) if result.data else None


async def get_alpha_controls(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("alpha_control")
        .select("*, food_provider(idFoodProvider, supplierName)")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [serialize_alpha_control(r) for r in result.data] if result.data else []


async def create_alpha_control(alpha_control: AlphaControlCreate):
    supabase = await get_supabase()
    data = alpha_control.model_dump(mode="json")

    if not data.get("fk_idFoodProvider"):
        data["fk_idFoodProvider"] = None


    insert_result = await supabase.table("alpha_control").insert(data).execute()
    if not insert_result.data:
        return None

    new_id = insert_result.data[0]["idAlphaControl"]

    result = (
        await supabase.table("alpha_control")
        .select("*, food_provider(idFoodProvider, supplierName)")
        .eq("idAlphaControl", new_id)
        .single()
        .execute()
    )
    return serialize_alpha_control(result.data) if result.data else None


async def update_alpha_control(idAlphaControl: int, alpha_control: AlphaControlUpdate):
    supabase = await get_supabase()
    data = alpha_control.model_dump(mode="json", exclude_unset=True)

    if "fk_idFoodProvider" in data and not data["fk_idFoodProvider"]:
        data["fk_idFoodProvider"] = None


    update_result = (
        await supabase.table("alpha_control")
        .update(data)
        .eq("idAlphaControl", idAlphaControl)
        .execute()
    )

    result = (
        await supabase.table("alpha_control")
        .select("*, food_provider(idFoodProvider, supplierName)")
        .eq("idAlphaControl", idAlphaControl)
        .single()
        .execute()
    )

    return serialize_alpha_control(result.data) if result.data else None


async def delete_alpha_control(idAlphaControl: int):
    supabase = await get_supabase()

    record = (
        await supabase.table("alpha_control")
        .select("*, food_provider(idFoodProvider, supplierName)")
        .eq("idAlphaControl", idAlphaControl)
        .single()
        .execute()
    )

    if not record.data:
        return None

    await supabase.table("alpha_control").delete().eq("idAlphaControl", idAlphaControl).execute()
    return serialize_alpha_control(record.data)
