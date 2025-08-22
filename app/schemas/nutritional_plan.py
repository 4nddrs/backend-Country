from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class NutritionalPlanBase(BaseModel):
    name: str
    startDate: date
    endDate: date
    description: Optional[str] = None


class NutritionalPlanCreate(NutritionalPlanBase):
    pass


class NutritionalPlanUpdate(NutritionalPlanBase):
    pass


class NutritionalPlanInDBBase(NutritionalPlanBase):
    idNutritionalPlan: int
    created_at: datetime

    class Config:
        orm_mode = True


class NutritionalPlan(NutritionalPlanInDBBase):
    pass
