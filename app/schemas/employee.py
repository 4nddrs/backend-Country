from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class EmployeeBase(BaseModel):
    fullName: str
    ci: str
    phoneNumber: int
    employeePhoto: Optional[str] = None
    startContractDate: date
    endContractDate: date
    startTime: datetime
    exitTime: datetime
    salary: int
    status: Optional[bool] = False
    fk_idRoleEmployee: int
    fk_idPositionEmployee: int


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeInDBBase(EmployeeBase):
    idEmployee: int
    created_at: datetime

    class Config:
        orm_mode = True


class Employee(EmployeeInDBBase):
    pass
