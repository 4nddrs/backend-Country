from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OwnerBase(BaseModel):
    name: str
    FirstName: str
    SecondName: Optional[str] = None
    ci: int
    phoneNumber: int
    ownerPhoto: Optional[str] = None  
    uid: Optional[str] = None  


class OwnerCreate(OwnerBase):
    pass


class OwnerUpdate(BaseModel):
    name: Optional[str] = None
    FirstName: Optional[str] = None
    SecondName: Optional[str] = None
    ci: Optional[int] = None
    phoneNumber: Optional[int] = None
    ownerPhoto: Optional[str] = None 
    uid: Optional[str] = None 


class OwnerInDBBase(OwnerBase):
    idOwner: int
    created_at: datetime

    class Config:
        from_attributes = True


class Owner(OwnerInDBBase):
    pass
