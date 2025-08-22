from pydantic import BaseModel
from datetime import datetime


class VaccineBase(BaseModel):
    vaccineName: str
    vaccineType: str


class VaccineCreate(VaccineBase):
    pass


class VaccineUpdate(VaccineBase):
    pass


class VaccineInDBBase(VaccineBase):
    idVaccine: int
    created_at: datetime

    class Config:
        orm_mode = True


class Vaccine(VaccineInDBBase):
    pass
