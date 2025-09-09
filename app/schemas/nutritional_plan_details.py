from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class NutritionalPlanDetailsBase(BaseModel):
    consumptionKlg: float
    daysConsumptionMonth: int
    totalConsumption: float
    period: date
    fk_idFood: int
    fk_idNutritionalPlan: int


class NutritionalPlanDetailsCreate(NutritionalPlanDetailsBase):
    pass


class NutritionalPlanDetailsUpdate(BaseModel):
    consumptionKlg: Optional[float] = None
    daysConsumptionMonth: Optional[int] = None
    totalConsumption: Optional[float] = None
    period: Optional[date] = None
    fk_idFood: Optional[int] = None
    fk_idNutritionalPlan: Optional[int] = None


class NutritionalPlanDetailsInDBBase(NutritionalPlanDetailsBase):
    idDetail: int
    created_at: datetime

    class Config:
        from_attributes = True


class NutritionalPlanDetails(NutritionalPlanDetailsInDBBase):
    pass
