from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import user_role as crud_user_role
from app.schemas import user_role as schemas_user_role

router = APIRouter(prefix="/user_roles", tags=["user_roles"])


@router.post(
    "/", response_model=schemas_user_role.UserRole, status_code=status.HTTP_201_CREATED
)
async def create_user_role(user_role_in: schemas_user_role.UserRoleCreate):
    user_role = await crud_user_role.create_user_role(user_role_in)
    if not user_role:
        raise HTTPException(status_code=400, detail="User role could not be created")
    return user_role


@router.get("/", response_model=List[schemas_user_role.UserRole])
async def list_user_roles(skip: int = 0, limit: int = 100):
    return await crud_user_role.get_user_roles(skip=skip, limit=limit)


@router.get("/{idUserRole}", response_model=schemas_user_role.UserRole)
async def get_user_role(idUserRole: int):
    user_role = await crud_user_role.get_user_role(idUserRole)
    if not user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    return user_role


@router.put("/{idUserRole}", response_model=schemas_user_role.UserRole)
async def update_user_role(
    idUserRole: int, user_role_in: schemas_user_role.UserRoleUpdate
):
    updated_role = await crud_user_role.update_user_role(idUserRole, user_role_in)
    if not updated_role:
        raise HTTPException(status_code=404, detail="User role not found")
    return updated_role


@router.delete("/{idUserRole}", response_model=schemas_user_role.UserRole)
async def delete_user_role(idUserRole: int):
    deleted_role = await crud_user_role.delete_user_role(idUserRole)
    if not deleted_role:
        raise HTTPException(status_code=404, detail="User role not found")
    return deleted_role
