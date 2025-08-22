from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import owner as crud_owner
from app.schemas import owner as schemas_owner

router = APIRouter(prefix="/owners", tags=["owners"])


@router.post(
    "/", response_model=schemas_owner.Owner, status_code=status.HTTP_201_CREATED
)
async def create_owner(owner_in: schemas_owner.OwnerCreate):
    owner = await crud_owner.create_owner(owner_in)
    if not owner:
        raise HTTPException(status_code=400, detail="Owner could not be created")
    return owner


@router.get("/", response_model=List[schemas_owner.Owner])
async def list_owners(skip: int = 0, limit: int = 100):
    owners = await crud_owner.get_owners(skip=skip, limit=limit)
    return owners


@router.get("/{owner_id}", response_model=schemas_owner.Owner)
async def get_owner(owner_id: int):
    owner = await crud_owner.get_owner(owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner


@router.put("/{owner_id}", response_model=schemas_owner.Owner)
async def update_owner(owner_id: int, owner_in: schemas_owner.OwnerUpdate):
    updated_owner = await crud_owner.update_owner(owner_id, owner_in)
    if not updated_owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return updated_owner


@router.delete("/{owner_id}", response_model=schemas_owner.Owner)
async def delete_owner(owner_id: int):
    deleted_owner = await crud_owner.delete_owner(owner_id)
    if not deleted_owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return deleted_owner
