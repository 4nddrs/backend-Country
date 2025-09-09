from datetime import date
from app.supabase_client import get_supabase
from app.schemas.scheduled_procedure import (
    ScheduledProcedureCreate,
    ScheduledProcedureUpdate,
)


async def get_scheduled_procedure(idScheduledProcedure: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("scheduled_procedure")
        .select("*")
        .eq("idScheduledProcedure", idScheduledProcedure)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_scheduled_procedures(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("scheduled_procedure")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_scheduled_procedure(proc: ScheduledProcedureCreate):
    supabase = await get_supabase()
    proc_dict = proc.model_dump(mode="json")
    result = await supabase.table("scheduled_procedure").insert(proc_dict).execute()
    return result.data[0] if result.data else None


async def update_scheduled_procedure(
    idScheduledProcedure: int, proc: ScheduledProcedureUpdate
):
    supabase = await get_supabase()
    proc_dict = proc.model_dump(mode="json", exclude_unset=True)
    result = (
        await supabase.table("scheduled_procedure")
        .update(proc_dict)
        .eq("idScheduledProcedure", idScheduledProcedure)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_scheduled_procedure(idScheduledProcedure: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("scheduled_procedure")
        .delete()
        .eq("idScheduledProcedure", idScheduledProcedure)
        .execute()
    )
    return result.data[0] if result.data else None
