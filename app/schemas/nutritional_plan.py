from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class NutritionalPlanBase(BaseModel):
    name: str
    assignmentDate: date 
    endDate: date
    state: str
    description: Optional[str] = None


class NutritionalPlanCreate(NutritionalPlanBase):
    pass


class NutritionalPlanUpdate(BaseModel):
    name: Optional[str] = None
    assignmentDate: Optional[date] = None
    endDate: Optional[date] = None
    state: Optional[str] = None
    description: Optional[str] = None


class NutritionalPlanInDBBase(NutritionalPlanBase):
    idNutritionalPlan: int
    created_at: datetime

    class Config:
        from_attributes = True


class NutritionalPlan(NutritionalPlanInDBBase):
    pass
