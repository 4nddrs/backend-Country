from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from decimal import Decimal


class EmployeeBase(BaseModel):
    fullName: str
    ci: int
    phoneNumber: int
    startContractDate: date
    endContractDate: date
    startTime: datetime
    exitTime: datetime
    salary: Decimal
    status: Optional[bool] = False
    fk_idPositionEmployee: int
    uid: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    fullName: Optional[str] = None
    ci: Optional[int] = None
    phoneNumber: Optional[int] = None
    startContractDate: Optional[date] = None
    endContractDate: Optional[date] = None
    startTime: Optional[datetime] = None
    exitTime: Optional[datetime] = None
    salary: Optional[Decimal] = None
    status: Optional[bool] = None
    fk_idPositionEmployee: Optional[int] = None
    uid: Optional[str] = None


class EmployeeInDBBase(EmployeeBase):
    idEmployee: int
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Employee(EmployeeInDBBase):
    pass