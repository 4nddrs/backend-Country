from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import total_control as crud_control
from app.schemas import total_control as schemas_control

router = APIRouter(prefix="/total_control", tags=["total_control"])


@router.post(
    "/",
    response_model=schemas_control.TotalControl,
    status_code=status.HTTP_201_CREATED,
)
async def create_total_control(control_in: schemas_control.TotalControlCreate):
    control = await crud_control.create_total_control(control_in)
    if not control:
        raise HTTPException(status_code=400, detail="TotalControl could not be created")
    return control


@router.get("/", response_model=List[schemas_control.TotalControl])
async def list_total_controls(skip: int = 0, limit: int = 100):
    return await crud_control.get_total_controls(skip=skip, limit=limit)


@router.get("/{idTotalControl}", response_model=schemas_control.TotalControl)
async def get_total_control(idTotalControl: int):
    control = await crud_control.get_total_control(idTotalControl)
    if not control:
        raise HTTPException(status_code=404, detail="TotalControl not found")
    return control


@router.put("/{idTotalControl}", response_model=schemas_control.TotalControl)
async def update_total_control(
    idTotalControl: int, control_in: schemas_control.TotalControlUpdate
):
    updated_control = await crud_control.update_total_control(
        idTotalControl, control_in
    )
    if not updated_control:
        raise HTTPException(status_code=404, detail="TotalControl not found")
    return updated_control


@router.delete("/{idTotalControl}", response_model=schemas_control.TotalControl)
async def delete_total_control(idTotalControl: int):
    deleted_control = await crud_control.delete_total_control(idTotalControl)
    if not deleted_control:
        raise HTTPException(status_code=404, detail="TotalControl not found")
    return deleted_control
