from pydantic import BaseModel
from datetime import datetime


class UserRoleBase(BaseModel):
    roleName: str


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(UserRoleBase):
    pass


class UserRoleInDBBase(UserRoleBase):
    idUserRole: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserRole(UserRoleInDBBase):
    pass
