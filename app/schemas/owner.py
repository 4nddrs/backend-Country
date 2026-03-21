from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OwnerBase(BaseModel):
    name: str
    FirstName: str
    SecondName: Optional[str] = None
    ci: int
    phoneNumber: int
    uid: Optional[str] = None


class OwnerCreate(OwnerBase):
    pass


class OwnerUpdate(BaseModel):
    name: Optional[str] = None
    FirstName: Optional[str] = None
    SecondName: Optional[str] = None
    ci: Optional[int] = None
    phoneNumber: Optional[int] = None
    uid: Optional[str] = None
    # image_url NO se toca desde aquí.
    # Se gestiona exclusivamente por POST /owner/{id}/image


class OwnerInDBBase(OwnerBase):
    idOwner: int
    image_url: Optional[str] = None  # URL pública de Supabase Storage (VARCHAR, nullable)
    created_at: datetime

    class Config:
        from_attributes = True


class Owner(OwnerInDBBase):
    pass