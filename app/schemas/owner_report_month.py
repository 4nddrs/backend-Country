from pydantic import BaseModel
from datetime import datetime


class OwnerReportMonthBase(BaseModel):
    period: float
    daysAlphaConsumption: float
    quantityAlphaKg: float
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


class OwnerReportMonthCreate(OwnerReportMonthBase):
    pass


class OwnerReportMonthUpdate(OwnerReportMonthBase):
    pass


class OwnerReportMonthInDBBase(OwnerReportMonthBase):
    idOwnerReportMonth: int
    created_at: datetime

    class Config:
        from_attributes = True


class OwnerReportMonth(OwnerReportMonthInDBBase):
    pass
