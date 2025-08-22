from app.supabase_client import get_supabase
from app.schemas.nutritional_plan_details import (
    NutritionalPlanDetailsCreate,
    NutritionalPlanDetailsUpdate,
)


async def get_nutritional_plan_detail(idDetail: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritional_plan_details")
        .select("*")
        .eq("idDetail", idDetail)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_nutritional_plan_details(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritional_plan_details")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_nutritional_plan_detail(detail: NutritionalPlanDetailsCreate):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritional_plan_details")
        .insert(detail.model_dump(mode="json"))
        .execute()
    )
    return result.data[0] if result.data else None


async def update_nutritional_plan_detail(
    idDetail: int, detail: NutritionalPlanDetailsUpdate
):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritional_plan_details")
        .update(detail.model_dump(mode="json", exclude_unset=True))
        .eq("idDetail", idDetail)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_nutritional_plan_detail(idDetail: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("nutritional_plan_details")
        .delete()
        .eq("idDetail", idDetail)
        .execute()
    )
    return result.data[0] if result.data else None
