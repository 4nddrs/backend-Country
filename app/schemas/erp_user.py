from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID


class ErpUserBase(BaseModel):
    username: str
    email: EmailStr
    fk_idUserRole: int
    isapproved: Optional[bool] = None
    approved_at: Optional[datetime] = None


class ErpUserCreate(ErpUserBase):
    pass


class ErpUserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    fk_idUserRole: Optional[int] = None
    isapproved: Optional[bool] = None
    approved_at: Optional[datetime] = None


class ErpUserInDBBase(ErpUserBase):
    uid: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ErpUser(ErpUserInDBBase):
    pass
