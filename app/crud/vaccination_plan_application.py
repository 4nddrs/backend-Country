from datetime import date, datetime
from app.supabase_client import get_supabase
from app.schemas.vaccination_plan_application import (
    VaccinationPlanApplicationCreate,
    VaccinationPlanApplicationUpdate,
)


def serialize_vaccination_plan_application(plan_app):
    """Convierte date/datetime a string para JSON"""
    data = plan_app.model_dump(exclude_unset=True)
    for key, value in data.items():
        if isinstance(value, (date, datetime)):
            data[key] = value.isoformat()
    return data


async def get_vaccination_plan_application(idVaccinationPlanApplication: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("vaccination_plan_application")
        .select("*")
        .eq("idVaccinationPlanApplication", idVaccinationPlanApplication)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_vaccination_plan_applications(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("vaccination_plan_application")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_vaccination_plan_application(
    plan_app: VaccinationPlanApplicationCreate,
):
    supabase = await get_supabase()
    payload = serialize_vaccination_plan_application(plan_app)
    result = (
        await supabase.table("vaccination_plan_application").insert(payload).execute()
    )
    return result.data[0] if result.data else None


async def update_vaccination_plan_application(
    idVaccinationPlanApplication: int, plan_app: VaccinationPlanApplicationUpdate
):
    supabase = await get_supabase()
    payload = serialize_vaccination_plan_application(plan_app)
    result = (
        await supabase.table("vaccination_plan_application")
        .update(payload)
        .eq("idVaccinationPlanApplication", idVaccinationPlanApplication)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_vaccination_plan_application(idVaccinationPlanApplication: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("vaccination_plan_application")
        .delete()
        .eq("idVaccinationPlanApplication", idVaccinationPlanApplication)
        .execute()
    )
    return result.data[0] if result.data else None
