from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    name: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductInDBBase(ProductBase):
    id: int
    created_at: datetime

    class Config:
        # Si recibes diccionarios de Supabase, no necesitas orm_mode
        from_attributes = True

class Product(ProductInDBBase):
    pass
