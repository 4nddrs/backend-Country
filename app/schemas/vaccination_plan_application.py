from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class VaccinationPlanApplicationBase(BaseModel):
    applicationDate: date
    observation: Optional[str] = None
    fk_idVaccinationPlan: int
    fk_idHorse: int
    fk_idEmployee: int


class VaccinationPlanApplicationCreate(VaccinationPlanApplicationBase):
    pass


class VaccinationPlanApplicationUpdate(VaccinationPlanApplicationBase):
    pass


class VaccinationPlanApplicationInDBBase(VaccinationPlanApplicationBase):
    idVaccinationPlanApplication: int
    created_at: datetime

    class Config:
        from_attributes = True


class VaccinationPlanApplication(VaccinationPlanApplicationInDBBase):
    pass
