from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class EmployeeAbsenceBase(BaseModel):
    startDate: date
    endDate: date
    isVacation: bool
    absent: bool
    observation: str
    fk_idEmployee: int


class EmployeeAbsenceCreate(EmployeeAbsenceBase):
    pass


class EmployeeAbsenceUpdate(EmployeeAbsenceBase):
    pass


class EmployeeAbsenceInDBBase(EmployeeAbsenceBase):
    idEmployeeAbsence: int
    created_at: datetime

    class Config:
        from_attributes = True


class EmployeeAbsence(EmployeeAbsenceInDBBase):
    pass
