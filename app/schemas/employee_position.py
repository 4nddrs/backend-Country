from pydantic import BaseModel
from datetime import datetime


class EmployeePositionBase(BaseModel):
    namePosition: str


class EmployeePositionCreate(EmployeePositionBase):
    pass


class EmployeePositionUpdate(EmployeePositionBase):
    pass


class EmployeePositionInDBBase(EmployeePositionBase):
    idPositionEmployee: int
    created_at: datetime

    class Config:
        orm_mode = True


class EmployeePosition(EmployeePositionInDBBase):
    pass
