from app.supabase_client import get_supabase
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate


async def get_user_role(idUserRole: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("user_role")
        .select("*")
        .eq("idUserRole", idUserRole)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_user_roles(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("user_role")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_user_role(user_role: UserRoleCreate):
    supabase = await get_supabase()
    payload = user_role.model_dump(exclude_unset=True)
    result = await supabase.table("user_role").insert(payload).execute()
    return result.data[0] if result.data else None


async def update_user_role(idUserRole: int, user_role: UserRoleUpdate):
    supabase = await get_supabase()
    payload = user_role.model_dump(exclude_unset=True)
    result = (
        await supabase.table("user_role")
        .update(payload)
        .eq("idUserRole", idUserRole)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_user_role(idUserRole: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("user_role")
        .delete()
        .eq("idUserRole", idUserRole)
        .execute()
    )
    return result.data[0] if result.data else None
