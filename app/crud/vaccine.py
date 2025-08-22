from app.supabase_client import get_supabase
from app.schemas.vaccine import VaccineCreate, VaccineUpdate


async def get_vaccine(vaccine_id: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("vaccine")
        .select("*")
        .eq("idVaccine", vaccine_id)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_vaccines(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("vaccine")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_vaccine(vaccine: VaccineCreate):
    supabase = await get_supabase()
    result = await supabase.table("vaccine").insert(vaccine.model_dump()).execute()
    return result.data[0] if result.data else None


async def update_vaccine(vaccine_id: int, vaccine: VaccineUpdate):
    supabase = await get_supabase()
    result = (
        await supabase.table("vaccine")
        .update(vaccine.model_dump(exclude_unset=True))
        .eq("idVaccine", vaccine_id)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_vaccine(vaccine_id: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("vaccine").delete().eq("idVaccine", vaccine_id).execute()
    )
    return result.data[0] if result.data else None
