from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import alpha_control as crud
from app.schemas import alpha_control as schemas

router = APIRouter(prefix="/alpha_controls", tags=["alpha_controls"])


@router.post(
    "/", response_model=schemas.AlphaControl, status_code=status.HTTP_201_CREATED
)
async def create_alpha_control(alpha_control_in: schemas.AlphaControlCreate):
    record = await crud.create_alpha_control(alpha_control_in)
    if not record:
        raise HTTPException(status_code=400, detail="AlphaControl could not be created")
    return record


@router.get("/", response_model=List[schemas.AlphaControl])
async def list_alpha_controls(skip: int = 0, limit: int = 100):
    return await crud.get_alpha_controls(skip=skip, limit=limit)


@router.get("/{idAlphaControl}", response_model=schemas.AlphaControl)
async def get_alpha_control(idAlphaControl: int):
    record = await crud.get_alpha_control(idAlphaControl)
    if not record:
        raise HTTPException(status_code=404, detail="AlphaControl not found")
    return record


@router.put("/{idAlphaControl}", response_model=schemas.AlphaControl)
async def update_alpha_control(
    idAlphaControl: int, alpha_control_in: schemas.AlphaControlUpdate
):
    updated = await crud.update_alpha_control(idAlphaControl, alpha_control_in)
    if not updated:
        raise HTTPException(status_code=404, detail="AlphaControl not found")
    return updated


@router.delete("/{idAlphaControl}", response_model=schemas.AlphaControl)
async def delete_alpha_control(idAlphaControl: int):
    deleted = await crud.delete_alpha_control(idAlphaControl)
    if not deleted:
        raise HTTPException(status_code=404, detail="AlphaControl not found")
    return deleted
