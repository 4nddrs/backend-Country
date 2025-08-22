from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class NutritionalPlanHorseBase(BaseModel):
    assignmentDate: date
    fk_idNutritionalPlan: int
    fk_idHorse: int


class NutritionalPlanHorseCreate(NutritionalPlanHorseBase):
    pass


class NutritionalPlanHorseUpdate(NutritionalPlanHorseBase):
    pass


class NutritionalPlanHorseInDBBase(NutritionalPlanHorseBase):
    idNutritionalPlan_horse: int
    created_at: datetime

    class Config:
        orm_mode = True


class NutritionalPlanHorse(NutritionalPlanHorseInDBBase):
    pass
