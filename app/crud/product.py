# app/crud/product.py
from app.supabase_client import get_supabase
from app.schemas.product import ProductCreate, ProductUpdate

async def get_product(product_id: int):
    supabase = await get_supabase()
    result = await supabase.table("product").select("*").eq("id", product_id).single().execute()
    return result.data if result.data else None

async def get_products(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = await supabase.table("product").select("*").range(skip, skip + limit - 1).execute()
    return result.data if result.data else []

async def create_product(product: ProductCreate):
    supabase = await get_supabase()
    result = await supabase.table("product").insert(product.model_dump()).execute()
    return result.data[0] if result.data else None

async def update_product(product_id: int, product: ProductUpdate):
    supabase = await get_supabase()
    result = await supabase.table("product").update(product.model_dump(exclude_unset=True)).eq("id", product_id).execute()
    return result.data[0] if result.data else None

async def delete_product(product_id: int):
    supabase = await get_supabase()
    result = await supabase.table("product").delete().eq("id", product_id).execute()
    return result.data[0] if result.data else None
