from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, Any


class ScheduledProcedureBase(BaseModel):
    year: date
    name: str
    description: Optional[str] = None
    scheduledMonths: Any  # jsonb → dict/list en Python
    alertLabel: str


class ScheduledProcedureCreate(ScheduledProcedureBase):
    pass


class ScheduledProcedureUpdate(ScheduledProcedureBase):
    pass


class ScheduledProcedureInDBBase(ScheduledProcedureBase):
    idScheduledProcedure: int
    created_at: datetime

    class Config:
        from_attributes = True


class ScheduledProcedure(ScheduledProcedureInDBBase):
    pass
