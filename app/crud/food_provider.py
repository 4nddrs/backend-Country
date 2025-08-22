from app.supabase_client import get_supabase
from app.schemas.food_provider import FoodProviderCreate, FoodProviderUpdate


async def get_food_provider(food_provider_id: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("food_provider")
        .select("*")
        .eq("idFoodProvider", food_provider_id)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_food_providers(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("food_provider")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_food_provider(food_provider: FoodProviderCreate):
    supabase = await get_supabase()
    result = (
        await supabase.table("food_provider")
        .insert(food_provider.model_dump())
        .execute()
    )
    return result.data[0] if result.data else None


async def update_food_provider(
    food_provider_id: int, food_provider: FoodProviderUpdate
):
    supabase = await get_supabase()
    result = (
        await supabase.table("food_provider")
        .update(food_provider.model_dump(exclude_unset=True))
        .eq("idFoodProvider", food_provider_id)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_food_provider(food_provider_id: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("food_provider")
        .delete()
        .eq("idFoodProvider", food_provider_id)
        .execute()
    )
    return result.data[0] if result.data else None
