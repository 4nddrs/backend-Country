from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class HorseBase(BaseModel):
    horseName: str
    birthdate: date
    sex: str
    color: str
    generalDescription: str
    passportNumber: Optional[int] = None
    box: Optional[bool] = None
    section: Optional[bool] = None
    basket: Optional[bool] = None
    fk_idRace: int
    fk_idOwner: int
    fl_idNutritionalPlan: Optional[int] = None
    state: str
    stateSchool: bool


class HorseCreate(HorseBase):
    pass


class HorseUpdate(BaseModel):
    horseName: Optional[str] = None
    birthdate: Optional[date] = None
    sex: Optional[str] = None
    color: Optional[str] = None
    generalDescription: Optional[str] = None
    passportNumber: Optional[int] = None
    box: Optional[bool] = None
    section: Optional[bool] = None
    basket: Optional[bool] = None
    fk_idRace: Optional[int] = None
    fk_idOwner: Optional[int] = None
    fl_idNutritionalPlan: Optional[int] = None
    state: Optional[str] = None
    stateSchool: Optional[bool] = None


class HorseInDBBase(HorseBase):
    idHorse: int
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Horse(HorseInDBBase):
    pass