from app.supabase_client import get_supabase
from app.schemas.task import TaskCreate, TaskUpdate


async def get_task(idTask: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("task").select("*").eq("idTask", idTask).single().execute()
    )
    return result.data if result.data else None


async def get_tasks(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("task").select("*").range(skip, skip + limit - 1).execute()
    )
    return result.data if result.data else []


async def create_task(task: TaskCreate):
    supabase = await get_supabase()
    result = await supabase.table("task").insert(task.model_dump(mode="json")).execute()
    return result.data[0] if result.data else None


async def update_task(idTask: int, task: TaskUpdate):
    supabase = await get_supabase()
    result = (
        await supabase.table("task")
        .update(task.model_dump(mode="json", exclude_unset=True))
        .eq("idTask", idTask)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_task(idTask: int):
    supabase = await get_supabase()
    result = await supabase.table("task").delete().eq("idTask", idTask).execute()
    return result.data[0] if result.data else None
