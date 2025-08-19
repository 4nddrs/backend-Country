from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import product as crud_product
from app.schemas import product as schemas_product

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=schemas_product.Product, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: schemas_product.ProductCreate):
    created_product = await crud_product.create_product(product_in)
    if not created_product:
        raise HTTPException(status_code=400, detail="Product could not be created")
    return created_product

@router.get("/", response_model=List[schemas_product.Product])
async def list_products(skip: int = 0, limit: int = 100):
    products = await crud_product.get_products(skip=skip, limit=limit)
    return products if products else []

@router.get("/{product_id}", response_model=schemas_product.Product)
async def get_product(product_id: int):
    product = await crud_product.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas_product.Product)
async def update_product(product_id: int, product_in: schemas_product.ProductUpdate):
    updated_product = await crud_product.update_product(product_id, product_in)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}", response_model=schemas_product.Product)
async def delete_product(product_id: int):
    deleted_product = await crud_product.delete_product(product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product
