from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class HorseBase(BaseModel):
    horseName: str
    dirthDate: date
    sex: str
    color: str
    generalDescription: str
    fk_idOwner: int
    fk_idRace: int
    fk_idEmployee: int
    fk_idVaccine: Optional[int] = None


class HorseCreate(HorseBase):
    horsePhoto: Optional[bytes] = None


class HorseUpdate(BaseModel):
    horseName: Optional[str] = None
    horsePhoto: Optional[bytes] = None
    dirthDate: Optional[date] = None
    sex: Optional[str] = None
    color: Optional[str] = None
    generalDescription: Optional[str] = None
    fk_idOwner: Optional[int] = None
    fk_idRace: Optional[int] = None
    fk_idEmployee: Optional[int] = None
    fk_idVaccine: Optional[int] = None


class HorseInDBBase(HorseBase):
    idHorse: int
    created_at: datetime
    horsePhoto: Optional[bytes] = None

    class Config:
        orm_mode = True


class Horse(HorseInDBBase):
    pass
