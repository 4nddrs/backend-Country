from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud import product as crud_product
from app.schemas import product as schemas_product
from app.database import get_session

router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    "/", response_model=schemas_product.Product, status_code=status.HTTP_201_CREATED
)
async def create_product(
    product_in: schemas_product.ProductCreate, db: AsyncSession = Depends(get_session)
):
    return await crud_product.create_product(db, product_in)


@router.get("/", response_model=List[schemas_product.Product])
async def list_products(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)
):
    return await crud_product.get_products(db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=schemas_product.Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_session)):
    db_product = await crud_product.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/{product_id}", response_model=schemas_product.Product)
async def update_product(
    product_id: int,
    product_in: schemas_product.ProductUpdate,
    db: AsyncSession = Depends(get_session),
):
    updated_product = await crud_product.update_product(db, product_id, product_in)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/{product_id}", response_model=schemas_product.Product)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_session)):
    deleted_product = await crud_product.delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product
