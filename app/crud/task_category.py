from app.supabase_client import get_supabase
from app.schemas.task_category import TaskCategoryCreate, TaskCategoryUpdate


async def get_task_category(idTaskCategory: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("task_category")
        .select("*")
        .eq("idTaskCategory", idTaskCategory)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_task_categories(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("task_category")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_task_category(category: TaskCategoryCreate):
    supabase = await get_supabase()
    result = (
        await supabase.table("task_category")
        .insert(category.model_dump(mode="json"))
        .execute()
    )
    return result.data[0] if result.data else None


async def update_task_category(idTaskCategory: int, category: TaskCategoryUpdate):
    supabase = await get_supabase()
    result = (
        await supabase.table("task_category")
        .update(category.model_dump(mode="json", exclude_unset=True))
        .eq("idTaskCategory", idTaskCategory)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_task_category(idTaskCategory: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("task_category")
        .delete()
        .eq("idTaskCategory", idTaskCategory)
        .execute()
    )
    return result.data[0] if result.data else None
