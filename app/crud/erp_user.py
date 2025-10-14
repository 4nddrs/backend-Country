from uuid import UUID
from app.supabase_client import get_supabase
from app.schemas.erp_user import ErpUserCreate, ErpUserUpdate


async def get_erp_user(uid: UUID):
    supabase = await get_supabase()
    result = (
        await supabase.table("erp_user")
        .select("*")
        .eq("uid", str(uid))
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_erp_users(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("erp_user")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_erp_user(user: ErpUserCreate, uid: UUID):
    supabase = await get_supabase()
    data_dict = user.model_dump(mode="json")
    data_dict["uid"] = str(uid)
    result = await supabase.table("erp_user").insert(data_dict).execute()
    return result.data[0] if result.data else None


async def update_erp_user(uid: UUID, user: ErpUserUpdate):
    supabase = await get_supabase()
    data_dict = user.model_dump(mode="json", exclude_unset=True)
    result = (
        await supabase.table("erp_user")
        .update(data_dict)
        .eq("uid", str(uid))
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_erp_user(uid: UUID):
    supabase = await get_supabase()
    result = (
        await supabase.table("erp_user")
        .delete()
        .eq("uid", str(uid))
        .execute()
    )
    return result.data[0] if result.data else None
