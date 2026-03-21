"""
Utilidad para manejo de imágenes en Supabase Storage.
Las entidades almacenan la URL en el campo `image_url` (VARCHAR, nullable).
"""
import uuid
from fastapi import UploadFile, HTTPException
from app.supabase_client import get_supabase

# ─── Buckets ──────────────────────────────────────────────────────────────────
BUCKET_OWNERS    = "owner-photos"
BUCKET_HORSES    = "horse-photos"
BUCKET_EMPLOYEES = "employee-photos"

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


# ─── Helpers internos ─────────────────────────────────────────────────────────

async def _delete_existing(bucket: str, folder: str) -> None:
    """Elimina todos los archivos anteriores de una carpeta en el bucket."""
    supabase = await get_supabase()
    try:
        existing = await supabase.storage.from_(bucket).list(folder)
        if existing:
            paths = [f"{folder}/{f['name']}" for f in existing]
            await supabase.storage.from_(bucket).remove(paths)
    except Exception:
        pass


async def _upload_image(bucket: str, entity_id: int | str, file: UploadFile) -> str:
    """
    Valida, sube y retorna la URL pública de una imagen.
    Elimina cualquier imagen anterior del mismo entity_id.
    """
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo no permitido: {file.content_type}. Use JPEG, PNG o WebP.",
        )

    content = await file.read()
    if len(content) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="La imagen supera el límite de 5 MB.")

    supabase = await get_supabase()

    # Eliminar imagen anterior para no acumular archivos huérfanos
    folder = str(entity_id)
    await _delete_existing(bucket, folder)

    ext = file.content_type.split("/")[1]  # jpeg | png | webp
    file_path = f"{folder}/{uuid.uuid4()}.{ext}"

    await supabase.storage.from_(bucket).upload(
        path=file_path,
        file=content,
        file_options={"content-type": file.content_type},
    )

    return await supabase.storage.from_(bucket).get_public_url(file_path)


async def _delete_by_url(bucket: str, image_url: str | None) -> None:
    """Elimina del Storage el archivo apuntado por image_url."""
    if not image_url:
        return
    try:
        supabase = await get_supabase()
        marker = f"/object/public/{bucket}/"
        path = image_url.split(marker)[1]
        await supabase.storage.from_(bucket).remove([path])
    except Exception:
        pass


# ─── API pública ──────────────────────────────────────────────────────────────

async def upload_owner_image(owner_id: int, file: UploadFile) -> str:
    return await _upload_image(BUCKET_OWNERS, owner_id, file)

async def upload_horse_image(horse_id: int, file: UploadFile) -> str:
    return await _upload_image(BUCKET_HORSES, horse_id, file)

async def upload_employee_image(employee_id: int, file: UploadFile) -> str:
    return await _upload_image(BUCKET_EMPLOYEES, employee_id, file)


async def delete_owner_image(image_url: str | None) -> None:
    await _delete_by_url(BUCKET_OWNERS, image_url)

async def delete_horse_image(image_url: str | None) -> None:
    await _delete_by_url(BUCKET_HORSES, image_url)

async def delete_employee_image(image_url: str | None) -> None:
    await _delete_by_url(BUCKET_EMPLOYEES, image_url)