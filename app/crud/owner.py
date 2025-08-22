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
    result = await supabase.table("owner").insert(owner.model_dump()).execute()
    return result.data[0] if result.data else None


async def update_owner(owner_id: int, owner: OwnerUpdate):
    supabase = await get_supabase()
    result = (
        await supabase.table("owner")
        .update(owner.model_dump(exclude_unset=True))
        .eq("idOwner", owner_id)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_owner(owner_id: int):
    supabase = await get_supabase()
    result = await supabase.table("owner").delete().eq("idOwner", owner_id).execute()
    return result.data[0] if result.data else None
