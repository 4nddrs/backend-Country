from pydantic import BaseModel
from datetime import datetime

class EmployeeRoleBase(BaseModel):
    nameRole: str

class EmployeeRoleCreate(EmployeeRoleBase):
    pass

class EmployeeRoleUpdate(EmployeeRoleBase):
    pass

class EmployeeRoleInDBBase(EmployeeRoleBase):
    idRoleEmployee: int
    created_at: datetime

    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes para Pydantic v2

class EmployeeRole(EmployeeRoleInDBBase):
    pass
