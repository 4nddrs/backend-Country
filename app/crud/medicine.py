from datetime import date
from app.supabase_client import get_supabase
from app.schemas.medicine import MedicineCreate, MedicineUpdate


def serialize_medicine(medicine: dict):
    """Convierte campos especiales (date → isoformat)."""
    for field in [
        "boxExpirationDate",
        "openedOn",
        "openedExpirationDate",
        "notifyDaysBefore",
    ]:
        if medicine.get(field) and isinstance(medicine[field], date):
            medicine[field] = medicine[field].isoformat()
    return medicine


async def get_medicine(idMedicine: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("medicine")
        .select("*")
        .eq("idMedicine", idMedicine)
        .single()
        .execute()
    )
    return serialize_medicine(result.data) if result.data else None


async def get_medicines(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("medicine")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [serialize_medicine(m) for m in result.data] if result.data else []


async def create_medicine(medicine: MedicineCreate):
    supabase = await get_supabase()
    medicine_dict = medicine.model_dump(mode="json")
    result = await supabase.table("medicine").insert(medicine_dict).execute()
    return serialize_medicine(result.data[0]) if result.data else None


async def update_medicine(idMedicine: int, medicine: MedicineUpdate):
    supabase = await get_supabase()
    medicine_dict = medicine.model_dump(mode="json", exclude_unset=True)
    result = (
        await supabase.table("medicine")
        .update(medicine_dict)
        .eq("idMedicine", idMedicine)
        .execute()
    )
    return serialize_medicine(result.data[0]) if result.data else None


async def delete_medicine(idMedicine: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("medicine").delete().eq("idMedicine", idMedicine).execute()
    )
    return serialize_medicine(result.data[0]) if result.data else None
