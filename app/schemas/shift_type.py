from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ShiftTypeBase(BaseModel):
    shiftName: str
    description: Optional[str] = None


class ShiftTypeCreate(ShiftTypeBase):
    pass


class ShiftTypeUpdate(ShiftTypeBase):
    pass


class ShiftTypeInDBBase(ShiftTypeBase):
    idShiftType: int
    created_at: datetime

    class Config:
        from_attributes = True


class ShiftType(ShiftTypeInDBBase):
    pass
