from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
from app.crud import alpha_control as crud
from app.schemas import alpha_control as schemas

router = APIRouter(
    prefix="/alpha_controls",
    tags=["alpha_controls"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_model=schemas.AlphaControl,
    status_code=status.HTTP_201_CREATED,
)
async def create_alpha_control(alpha_control_in: schemas.AlphaControlCreate):
    data = alpha_control_in.model_dump()
    if not data.get("fk_idFoodProvider"):
        data["fk_idFoodProvider"] = None
    record = await crud.create_alpha_control(schemas.AlphaControlCreate(**data))

    if not record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="AlphaControl could not be created",
        )
    return record


@router.get("/", response_model=List[schemas.AlphaControl])
async def list_alpha_controls(skip: int = 0, limit: int = 100):
    return await crud.get_alpha_controls(skip=skip, limit=limit)


@router.get("/{idAlphaControl}", response_model=schemas.AlphaControl)
async def get_alpha_control(idAlphaControl: int):
    record = await crud.get_alpha_control(idAlphaControl)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AlphaControl not found",
        )
    return record


@router.put("/{idAlphaControl}", response_model=schemas.AlphaControl)
async def update_alpha_control(
    idAlphaControl: int, alpha_control_in: schemas.AlphaControlUpdate
):
   
    data = alpha_control_in.model_dump(exclude_unset=True)
    if "fk_idFoodProvider" in data and not data["fk_idFoodProvider"]:
        data["fk_idFoodProvider"] = None

    updated = await crud.update_alpha_control(
        idAlphaControl, schemas.AlphaControlUpdate(**data)
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AlphaControl not found",
        )
    return updated


@router.delete("/{idAlphaControl}")
async def delete_alpha_control(idAlphaControl: int):
    deleted = await crud.delete_alpha_control(idAlphaControl)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AlphaControl not found",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "AlphaControl deleted successfully"},
    )
