from app.supabase_client import get_supabase
from app.schemas.owner import OwnerCreate, OwnerUpdate


async def get_owner(owner_id: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("owner")
        .select("*")
        .eq("idOwner", owner_id)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_owners(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("owner")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_owner(owner: OwnerCreate):
    supabase = await get_supabase()

    owner_data = owner.model_dump(exclude_unset=True)

    if owner_data.get("uid"):
        check_uid = (
            await supabase.table("erp_user")
            .select("uid")
            .eq("uid", owner_data["uid"])
            .single()
            .execute()
        )
        if not check_uid.data:
            raise ValueError("El UID proporcionado no existe en erp_user.")

    result = await supabase.table("owner").insert(owner_data).execute()
    return result.data[0] if result.data else None


async def update_owner(owner_id: int, owner: OwnerUpdate):
    supabase = await get_supabase()
    update_data = owner.model_dump(exclude_unset=True)

    if update_data.get("uid"):
        check_uid = (
            await supabase.table("erp_user")
            .select("uid")
            .eq("uid", update_data["uid"])
            .single()
            .execute()
        )
        if not check_uid.data:
            raise ValueError("El UID proporcionado no existe en erp_user.")

    result = (
        await supabase.table("owner")
        .update(update_data)
        .eq("idOwner", owner_id)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_owner(owner_id: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("owner")
        .delete()
        .eq("idOwner", owner_id)
        .execute()
    )
    return result.data[0] if result.data else None
