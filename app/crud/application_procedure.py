from datetime import date
from app.supabase_client import get_supabase
from app.schemas.application_procedure import (
    ApplicationProcedureCreate,
    ApplicationProcedureUpdate,
)


async def get_application_procedure(idApplicationProcedure: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("application_procedure")
        .select("*")
        .eq("idApplicationProcedure", idApplicationProcedure)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_application_procedures(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("application_procedure")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_application_procedure(proc: ApplicationProcedureCreate):
    supabase = await get_supabase()
    proc_dict = proc.model_dump(mode="json")
    result = await supabase.table("application_procedure").insert(proc_dict).execute()
    return result.data[0] if result.data else None


async def update_application_procedure(
    idApplicationProcedure: int, proc: ApplicationProcedureUpdate
):
    supabase = await get_supabase()
    proc_dict = proc.model_dump(mode="json", exclude_unset=True)
    result = (
        await supabase.table("application_procedure")
        .update(proc_dict)
        .eq("idApplicationProcedure", idApplicationProcedure)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_application_procedure(idApplicationProcedure: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("application_procedure")
        .delete()
        .eq("idApplicationProcedure", idApplicationProcedure)
        .execute()
    )
    return result.data[0] if result.data else None
