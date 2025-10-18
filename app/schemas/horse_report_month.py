from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HorseLite(BaseModel):
    idHorse: int
    horseName: str

    class Config:
        from_attributes = True


class HorseReportMonthBase(BaseModel):
    days: int
    alphaKg: float
    fk_idHorse: int
    fk_idOwnerReportMonth: Optional[int] = None


class HorseReportMonthCreate(HorseReportMonthBase):
    pass


class HorseReportMonthUpdate(HorseReportMonthBase):
    pass


class HorseReportMonthInDBBase(HorseReportMonthBase):
    idHorseReportMonth: int
    created_at: datetime

    class Config:
        from_attributes = True


class HorseReportMonth(HorseReportMonthInDBBase):
    horse: Optional[HorseLite] = None
