from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class AttentionHorseBase(BaseModel):
    date: date
    dose: str
    cost: float
    description: str
    fk_idHorse: int
    fk_idMedicine: Optional[int] = None
    fk_idEmployee: int


class AttentionHorseCreate(AttentionHorseBase):
    pass


class AttentionHorseUpdate(AttentionHorseBase):
    pass


class AttentionHorseInDBBase(AttentionHorseBase):
    idAttentionHorse: int
    created_at: datetime

    class Config:
        from_attributes = True


class AttentionHorse(AttentionHorseInDBBase):
    pass
