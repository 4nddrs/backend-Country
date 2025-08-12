from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalars().first()


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()


async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(name=product.name)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(db: AsyncSession, product_id: int, product: ProductUpdate):
    db_product = await get_product(db, product_id)
    if not db_product:
        return None
    db_product.name = product.name
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    db_product = await get_product(db, product_id)
    if not db_product:
        return None
    await db.delete(db_product)
    await db.commit()
    return db_product
