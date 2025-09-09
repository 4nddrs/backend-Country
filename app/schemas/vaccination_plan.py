from pydantic import BaseModel
from datetime import datetime
from typing import Any


class VaccinationPlanBase(BaseModel):
    planName: str
    scheduledMonths: Any  # jsonb
    dosesByMonth: Any  # json
    alertStatus: str
    fk_idMedicine: int


class VaccinationPlanCreate(VaccinationPlanBase):
    pass


class VaccinationPlanUpdate(VaccinationPlanBase):
    pass


class VaccinationPlanInDBBase(VaccinationPlanBase):
    idVaccinationPlan: int
    created_at: datetime

    class Config:
        from_attributes = True


class VaccinationPlan(VaccinationPlanInDBBase):
    pass
