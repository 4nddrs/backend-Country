from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import erp_user as crud_erp_user
from app.schemas import erp_user as schemas_erp_user

router = APIRouter(prefix="/erp_users", tags=["erp_users"])


@router.post(
    "/", response_model=schemas_erp_user.ErpUser, status_code=status.HTTP_201_CREATED
)
async def create_erp_user(user_in: schemas_erp_user.ErpUserCreate):
    user = await crud_erp_user.create_erp_user(user_in)
    if not user:
        raise HTTPException(status_code=400, detail="ERP User could not be created")
    return user


@router.get("/", response_model=List[schemas_erp_user.ErpUser])
async def list_erp_users(skip: int = 0, limit: int = 100):
    users = await crud_erp_user.get_erp_users(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas_erp_user.ErpUser)
async def get_erp_user(user_id: int):
    user = await crud_erp_user.get_erp_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="ERP User not found")
    return user


@router.put("/{user_id}", response_model=schemas_erp_user.ErpUser)
async def update_erp_user(user_id: int, user_in: schemas_erp_user.ErpUserUpdate):
    updated_user = await crud_erp_user.update_erp_user(user_id, user_in)
    if not updated_user:
        raise HTTPException(status_code=404, detail="ERP User not found")
    return updated_user


@router.delete("/{user_id}", response_model=schemas_erp_user.ErpUser)
async def delete_erp_user(user_id: int):
    deleted_user = await crud_erp_user.delete_erp_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="ERP User not found")
    return deleted_user
