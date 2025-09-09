from pydantic import BaseModel
from datetime import datetime


class ShiftEmployedBase(BaseModel):
    startDateTime: datetime
    endDateTime: datetime
    fk_idShiftType: int


class ShiftEmployedCreate(ShiftEmployedBase):
    pass


class ShiftEmployedUpdate(ShiftEmployedBase):
    pass


class ShiftEmployedInDBBase(ShiftEmployedBase):
    idShiftEmployed: int
    created_at: datetime

    class Config:
        from_attributes = True


class ShiftEmployed(ShiftEmployedInDBBase):
    pass
