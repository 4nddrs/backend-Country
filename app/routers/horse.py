from fastapi import APIRouter, HTTPException, UploadFile, File, status
from typing import List

from app.crud import horse as crud_horse
from app.schemas import horse as schemas_horse
from app.utils.storage import upload_horse_image, delete_horse_image

router = APIRouter(prefix="/horses", tags=["horses"])


@router.post("/", response_model=schemas_horse.Horse, status_code=status.HTTP_201_CREATED)
async def create_horse(horse_in: schemas_horse.HorseCreate):
    horse = await crud_horse.create_horse(horse_in)
    if not horse:
        raise HTTPException(status_code=400, detail="Horse could not be created")
    return horse


@router.get("/", response_model=List[schemas_horse.Horse])
async def list_horses(skip: int = 0, limit: int = 100):
    return await crud_horse.get_horses(skip=skip, limit=limit)


@router.get("/by_owner/{idOwner}", response_model=List[schemas_horse.Horse])
async def get_horses_by_owner(idOwner: int):
    horses = await crud_horse.get_horses_by_owner(idOwner)
    if horses is None:
        raise HTTPException(status_code=404, detail="No horses found for this owner")
    return horses


@router.get("/{horse_id}", response_model=schemas_horse.Horse)
async def get_horse(horse_id: int):
    horse = await crud_horse.get_horse(horse_id)
    if not horse:
        raise HTTPException(status_code=404, detail="Horse not found")
    return horse


@router.put("/{horse_id}", response_model=schemas_horse.Horse)
async def update_horse(horse_id: int, horse_in: schemas_horse.HorseUpdate):
    updated = await crud_horse.update_horse(horse_id, horse_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Horse not found")
    return updated


@router.delete("/{horse_id}", response_model=schemas_horse.Horse)
async def delete_horse(horse_id: int):
    horse = await crud_horse.get_horse(horse_id)
    if not horse:
        raise HTTPException(status_code=404, detail="Horse not found")
    if horse.get("image_url"):
        await delete_horse_image(horse["image_url"])
    return await crud_horse.delete_horse(horse_id)


# ── Gestión de imagen ──────────────────────────────────────────────────────────

@router.post("/{horse_id}/image", response_model=schemas_horse.Horse)
async def upload_horse_image_endpoint(
    horse_id: int,
    image: UploadFile = File(..., description="JPEG, PNG o WebP. Máx 5 MB."),
):
    horse = await crud_horse.get_horse(horse_id)
    if not horse:
        raise HTTPException(status_code=404, detail="Horse not found")

    image_url = await upload_horse_image(horse_id, image)
    updated = await crud_horse.update_horse_image(horse_id, image_url)
    if not updated:
        raise HTTPException(status_code=500, detail="No se pudo guardar la URL de la imagen.")
    return updated


@router.delete("/{horse_id}/image")
async def delete_horse_image_endpoint(horse_id: int):
    horse = await crud_horse.get_horse(horse_id)
    if not horse:
        raise HTTPException(status_code=404, detail="Horse not found")
    if not horse.get("image_url"):
        raise HTTPException(status_code=404, detail="El horse no tiene imagen registrada.")

    await delete_horse_image(horse["image_url"])
    await crud_horse.update_horse_image(horse_id, None)
    return {"detail": "Imagen eliminada correctamente."}