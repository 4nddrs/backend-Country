from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NutritionalPlanDetailsBase(BaseModel):
    amount: float
    frequency: str
    schedule: datetime
    fk_idFood: int
    fk_idNutritionalPlan: Optional[int] = None


class NutritionalPlanDetailsCreate(NutritionalPlanDetailsBase):
    pass


class NutritionalPlanDetailsUpdate(NutritionalPlanDetailsBase):
    pass


class NutritionalPlanDetailsInDBBase(NutritionalPlanDetailsBase):
    idDetail: int
    created_at: datetime

    class Config:
        orm_mode = True


class NutritionalPlanDetails(NutritionalPlanDetailsInDBBase):
    pass
