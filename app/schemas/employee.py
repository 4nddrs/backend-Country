from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from decimal import Decimal


class EmployeeBase(BaseModel):
    fullName: str
    ci: int
    phoneNumber: int
    employeePhoto: Optional[str] = None
    startContractDate: date
    endContractDate: date
    startTime: datetime
    exitTime: datetime
    salary: Decimal
    status: Optional[bool] = False
    fk_idPositionEmployee: int


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeInDBBase(EmployeeBase):
    idEmployee: int
    created_at: datetime

    class Config:
        from_attributes = True


class Employee(EmployeeInDBBase):
    pass
