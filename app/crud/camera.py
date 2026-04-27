from app.supabase_client import get_supabase
from app.schemas.camera import CameraCreate, CameraUpdate


def _serialize(data: dict) -> dict:
    if data and "created_at" in data and data["created_at"]:
        data["created_at"] = str(data["created_at"])
    return data


def _public(data: dict) -> dict:
    """Remove rtsp_password from outgoing data."""
    if data:
        data.pop("rtsp_password", None)
    return data


async def get_all_cameras():
    supabase = await get_supabase()
    result = await supabase.table("camera").select("*").execute()
    return [_public(_serialize(c)) for c in result.data] if result.data else []


async def get_camera(idCamera: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("camera")
        .select("*")
        .eq("idCamera", idCamera)
        .single()
        .execute()
    )
    return _public(_serialize(result.data)) if result.data else None


async def get_camera_credentials(idCamera: int):
    """Returns full record including rtsp_password — for internal backend use only."""
    supabase = await get_supabase()
    result = (
        await supabase.table("camera")
        .select("*")
        .eq("idCamera", idCamera)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def create_camera(camera_in: CameraCreate):
    supabase = await get_supabase()
    result = await supabase.table("camera").insert(camera_in.model_dump()).execute()
    return _public(_serialize(result.data[0])) if result.data else None


async def update_camera(idCamera: int, camera_in: CameraUpdate):
    supabase = await get_supabase()
    update_data = {k: v for k, v in camera_in.model_dump().items() if v is not None}
    if not update_data:
        return await get_camera(idCamera)
    result = (
        await supabase.table("camera")
        .update(update_data)
        .eq("idCamera", idCamera)
        .execute()
    )
    return _public(_serialize(result.data[0])) if result.data else None


async def delete_camera(idCamera: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("camera").delete().eq("idCamera", idCamera).execute()
    )
    return result.data[0] if result.data else None
