from datetime import datetime
from app.supabase_client import get_supabase
from app.schemas.vaccination_plan import VaccinationPlanCreate, VaccinationPlanUpdate


def serialize_vaccination_plan(plan):
    """Convierte datetime a string para JSON"""
    data = plan.model_dump(exclude_unset=True)
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    return data


async def get_vaccination_plan(idVaccinationPlan: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("vaccination_plan")
        .select("*")
        .eq("idVaccinationPlan", idVaccinationPlan)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_vaccination_plans(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("vaccination_plan")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_vaccination_plan(plan: VaccinationPlanCreate):
    supabase = await get_supabase()
    payload = serialize_vaccination_plan(plan)
    result = await supabase.table("vaccination_plan").insert(payload).execute()
    return result.data[0] if result.data else None


async def update_vaccination_plan(idVaccinationPlan: int, plan: VaccinationPlanUpdate):
    supabase = await get_supabase()
    payload = serialize_vaccination_plan(plan)
    result = (
        await supabase.table("vaccination_plan")
        .update(payload)
        .eq("idVaccinationPlan", idVaccinationPlan)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_vaccination_plan(idVaccinationPlan: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("vaccination_plan")
        .delete()
        .eq("idVaccinationPlan", idVaccinationPlan)
        .execute()
    )
    return result.data[0] if result.data else None
