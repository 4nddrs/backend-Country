from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EmployeesShiftemBase(BaseModel):
    fk_idEmployee: Optional[int] = None
    fk_idShiftEmployees: Optional[int] = None


class EmployeesShiftemCreate(EmployeesShiftemBase):
    pass


class EmployeesShiftemUpdate(EmployeesShiftemBase):
    pass


class EmployeesShiftemInDBBase(EmployeesShiftemBase):
    idEmployeesShiftem: int
    created_at: datetime

    class Config:
        from_attributes = True


class EmployeesShiftem(EmployeesShiftemInDBBase):
    pass
