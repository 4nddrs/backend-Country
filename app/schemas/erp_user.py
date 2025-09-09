from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID


class ErpUserBase(BaseModel):
    username: str
    email: EmailStr
    fk_idOwner: Optional[int] = None
    fk_idEmployee: Optional[int] = None
    fk_idAuthUser: Optional[UUID] = None
    fk_idUserRole: int


class ErpUserCreate(ErpUserBase):
    pass


class ErpUserUpdate(ErpUserBase):
    pass


class ErpUserInDBBase(ErpUserBase):
    idErpUser: int
    created_at: datetime

    class Config:
        from_attributes = True


class ErpUser(ErpUserInDBBase):
    pass
