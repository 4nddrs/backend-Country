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
        orm_mode = True


class Product(ProductInDBBase):
    pass
