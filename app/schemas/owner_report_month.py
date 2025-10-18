from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
from app.schemas.horse_report_month import HorseReportMonthCreate, HorseReportMonth


class HorseLite(BaseModel):
    idHorse: int
    horseName: str
    box: bool
    section: bool

    class Config:
        from_attributes = True


class OwnerLite(BaseModel):
    idOwner: int
    name: str
    FirstName: str
    SecondName: Optional[str] = None
    horses: Optional[List[HorseLite]] = []

    class Config:
        from_attributes = True


class OwnerReportMonthBase(BaseModel):
    period: date
    priceAlpha: float
    box: float
    section: float
    aBasket: float
    contributionCabFlyer: float
    VaccineApplication: float
    deworming: float
    AmeniaExam: float
    externalTeacher: float
    fine: float
    saleChala: float
    costPerBucket: float
    healthCardPayment: float
    other: float
    fk_idOwner: int
    state: str
    paymentDate: Optional[datetime] = None


class OwnerReportMonthCreate(OwnerReportMonthBase):
    horses_report: Optional[List[HorseReportMonthCreate]] = []

    class Config:
        extra = "ignore"  


class OwnerReportMonthUpdate(OwnerReportMonthBase):
    pass


class OwnerReportMonthInDBBase(OwnerReportMonthBase):
    idOwnerReportMonth: int
    created_at: datetime

    class Config:
        from_attributes = True


class OwnerReportMonth(OwnerReportMonthInDBBase):
    owner: Optional[OwnerLite] = None
    horses_report: Optional[List[HorseReportMonth]] = []


def serialize_owner_report_month(report):
    data = report.model_dump(exclude_unset=True, exclude={"horses_report"})
    for key, value in data.items():
        if isinstance(value, (datetime, date)):
            data[key] = value.isoformat()
    return data
