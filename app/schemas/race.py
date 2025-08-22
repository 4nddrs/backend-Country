from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RaceBase(BaseModel):
    nameRace: str


class RaceCreate(RaceBase):
    pass


class RaceUpdate(BaseModel):
    nameRace: Optional[str] = None


class RaceInDBBase(RaceBase):
    idRace: int
    created_at: datetime

    class Config:
        orm_mode = True


class Race(RaceInDBBase):
    pass
