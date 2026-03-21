from fastapi import APIRouter, HTTPException, UploadFile, File, status
from typing import List

from app.crud import owner as crud_owner
from app.schemas import owner as schemas_owner
from app.utils.storage import upload_owner_image, delete_owner_image

router = APIRouter(prefix="/owner", tags=["owner"])


# ─── CRUD estándar ────────────────────────────────────────────────────────────

@router.post("/", response_model=schemas_owner.Owner, status_code=status.HTTP_201_CREATED)
async def create_owner(owner_in: schemas_owner.OwnerCreate):
    """
    Crea un propietario sin imagen.
    La imagen se sube por separado con POST /owner/{id}/image
    """
    try:
        owner = await crud_owner.create_owner(owner_in)
        if not owner:
            raise HTTPException(status_code=400, detail="No se pudo crear el propietario.")
        return owner
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/", response_model=List[schemas_owner.Owner])
async def list_owners(skip: int = 0, limit: int = 100):
    return await crud_owner.get_owners(skip=skip, limit=limit)


@router.get("/by_uid/{uid}", response_model=schemas_owner.Owner)
async def get_owner_by_uid(uid: str):
    owner = await crud_owner.get_owner_by_uid(uid)
    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado.")
    return owner


@router.get("/{owner_id}", response_model=schemas_owner.Owner)
async def get_owner(owner_id: int):
    owner = await crud_owner.get_owner(owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado.")
    return owner


@router.put("/{owner_id}", response_model=schemas_owner.Owner)
async def update_owner(owner_id: int, owner_in: schemas_owner.OwnerUpdate):
    try:
        updated_owner = await crud_owner.update_owner(owner_id, owner_in)
        if not updated_owner:
            raise HTTPException(status_code=404, detail="Propietario no encontrado.")
        return updated_owner
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.delete("/{owner_id}", response_model=schemas_owner.Owner)
async def delete_owner(owner_id: int):
    owner = await crud_owner.get_owner(owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado.")

    # Limpiar imagen del Storage antes de borrar el registro
    if owner.get("image_url"):
        await delete_owner_image(owner["image_url"])

    deleted = await crud_owner.delete_owner(owner_id)
    return deleted


# ─── Gestión de imagen (Storage) ──────────────────────────────────────────────

@router.post(
    "/{owner_id}/image",
    response_model=schemas_owner.Owner,
    summary="Subir o reemplazar imagen del propietario",
)
async def upload_owner_image_endpoint(
    owner_id: int,
    image: UploadFile = File(..., description="JPEG, PNG o WebP. Máx 5 MB."),
):
    """
    Sube la imagen al bucket `owner-photos` en Supabase Storage
    y guarda la URL pública en el campo `image_url` de la BD.

    - Si ya existía una imagen anterior, la reemplaza automáticamente.
    - Retorna el propietario completo con la nueva image_url.
    """
    owner = await crud_owner.get_owner(owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado.")

    # Subir al Storage (valida tipo y tamaño internamente)
    image_url = await upload_owner_image(owner_id, image)

    # Persistir la URL en la BD
    updated = await crud_owner.update_owner_image(owner_id, image_url)
    if not updated:
        raise HTTPException(status_code=500, detail="No se pudo guardar la URL de la imagen.")

    return updated


@router.delete(
    "/{owner_id}/image",
    summary="Eliminar imagen del propietario",
)
async def delete_owner_image_endpoint(owner_id: int):
    """
    Elimina la imagen del bucket en Storage y pone image_url en NULL en la BD.
    """
    owner = await crud_owner.get_owner(owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado.")

    if not owner.get("image_url"):
        raise HTTPException(status_code=404, detail="El propietario no tiene imagen registrada.")

    await delete_owner_image(owner["image_url"])
    await crud_owner.update_owner_image(owner_id, None)

    return {"detail": "Imagen eliminada correctamente."}