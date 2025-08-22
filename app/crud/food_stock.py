from app.supabase_client import get_supabase
from app.schemas.food_stock import FoodStockCreate, FoodStockUpdate


async def get_food_stock(food_id: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("food_stock")
        .select("*")
        .eq("idFood", food_id)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_food_stocks(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("food_stock")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_food_stock(food_stock: FoodStockCreate):
    supabase = await get_supabase()
    result = (
        await supabase.table("food_stock").insert(food_stock.model_dump()).execute()
    )
    return result.data[0] if result.data else None


async def update_food_stock(food_id: int, food_stock: FoodStockUpdate):
    supabase = await get_supabase()
    result = (
        await supabase.table("food_stock")
        .update(food_stock.model_dump(exclude_unset=True))
        .eq("idFood", food_id)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_food_stock(food_id: int):
    supabase = await get_supabase()
    result = await supabase.table("food_stock").delete().eq("idFood", food_id).execute()
    return result.data[0] if result.data else None
