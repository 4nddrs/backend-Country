from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class HorseBase(BaseModel):
    horseName: str
    horsePhoto: Optional[str] = None  # Se enviará como Base64 desde el front
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

class HorseCreate(HorseBase):
    pass

class HorseUpdate(HorseBase):
    pass

class HorseInDBBase(HorseBase):
    idHorse: int
    created_at: datetime

    class Config:
        from_attributes = True

class Horse(HorseInDBBase):
    pass
