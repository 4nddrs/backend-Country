from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import attention_horse as crud_attention
from app.schemas import attention_horse as schemas_attention

router = APIRouter(prefix="/attention_horses", tags=["attention_horses"])


@router.post(
    "/",
    response_model=schemas_attention.AttentionHorse,
    status_code=status.HTTP_201_CREATED,
)
async def create_attention_horse(attention_in: schemas_attention.AttentionHorseCreate):
    attention = await crud_attention.create_attention_horse(attention_in)
    if not attention:
        raise HTTPException(
            status_code=400, detail="AttentionHorse could not be created"
        )
    return attention


@router.get("/", response_model=List[schemas_attention.AttentionHorse])
async def list_attention_horses(skip: int = 0, limit: int = 100):
    attentions = await crud_attention.get_attention_horses(skip=skip, limit=limit)
    return attentions


@router.get("/{attention_id}", response_model=schemas_attention.AttentionHorse)
async def get_attention_horse(attention_id: int):
    attention = await crud_attention.get_attention_horse(attention_id)
    if not attention:
        raise HTTPException(status_code=404, detail="AttentionHorse not found")
    return attention


@router.put("/{attention_id}", response_model=schemas_attention.AttentionHorse)
async def update_attention_horse(
    attention_id: int, attention_in: schemas_attention.AttentionHorseUpdate
):
    updated_attention = await crud_attention.update_attention_horse(
        attention_id, attention_in
    )
    if not updated_attention:
        raise HTTPException(status_code=404, detail="AttentionHorse not found")
    return updated_attention


@router.delete("/{attention_id}", response_model=schemas_attention.AttentionHorse)
async def delete_attention_horse(attention_id: int):
    deleted_attention = await crud_attention.delete_attention_horse(attention_id)
    if not deleted_attention:
        raise HTTPException(status_code=404, detail="AttentionHorse not found")
    return deleted_attention
