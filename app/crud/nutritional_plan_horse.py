from app.supabase_client import get_supabase
from app.schemas.nutritional_plan_horse import (
    NutritionalPlanHorseCreate,
    NutritionalPlanHorseUpdate,
)


async def get_nutritional_plan_horse(idNutritionalPlan_horse: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritionalPlan_horse")
        .select("*")
        .eq("idNutritionalPlan_horse", idNutritionalPlan_horse)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_nutritional_plan_horses(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritionalPlan_horse")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_nutritional_plan_horse(plan_horse: NutritionalPlanHorseCreate):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritionalPlan_horse")
        .insert(plan_horse.model_dump(mode="json"))
        .execute()
    )
    return result.data[0] if result.data else None


async def update_nutritional_plan_horse(
    idNutritionalPlan_horse: int, plan_horse: NutritionalPlanHorseUpdate
):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritionalPlan_horse")
        .update(plan_horse.model_dump(mode="json", exclude_unset=True))
        .eq("idNutritionalPlan_horse", idNutritionalPlan_horse)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_nutritional_plan_horse(idNutritionalPlan_horse: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritionalPlan_horse")
        .delete()
        .eq("idNutritionalPlan_horse", idNutritionalPlan_horse)
        .execute()
    )
    return result.data[0] if result.data else None
