from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class ApplicationProcedureBase(BaseModel):
    executionDate: date
    observations: Optional[str] = None
    fk_idScheduledProcedure: int
    fk_idHorse: int


class ApplicationProcedureCreate(ApplicationProcedureBase):
    pass


class ApplicationProcedureUpdate(ApplicationProcedureBase):
    pass


class ApplicationProcedureInDBBase(ApplicationProcedureBase):
    idApplicationProcedure: int
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationProcedure(ApplicationProcedureInDBBase):
    pass
