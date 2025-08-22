from app.supabase_client import get_supabase
from app.schemas.nutritional_plan import NutritionalPlanCreate, NutritionalPlanUpdate


async def get_nutritional_plan(idNutritionalPlan: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritional_plan")
        .select("*")
        .eq("idNutritionalPlan", idNutritionalPlan)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_nutritional_plans(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritional_plan")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_nutritional_plan(plan: NutritionalPlanCreate):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritional_plan")
        .insert(plan.model_dump(mode="json"))
        .execute()
    )
    return result.data[0] if result.data else None


async def update_nutritional_plan(idNutritionalPlan: int, plan: NutritionalPlanUpdate):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritional_plan")
        .update(plan.model_dump(mode="json", exclude_unset=True))
        .eq("idNutritionalPlan", idNutritionalPlan)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_nutritional_plan(idNutritionalPlan: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritional_plan")
        .delete()
        .eq("idNutritionalPlan", idNutritionalPlan)
        .execute()
    )
    return result.data[0] if result.data else None
