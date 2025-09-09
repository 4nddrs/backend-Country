from pydantic import BaseModel
from datetime import datetime


class TotalControlBase(BaseModel):
    toCaballerizo: float
    vaccines: float
    anemia: float
    deworming: float
    consumptionAlfaDiaKlg: float
    costAlfaBs: float
    daysConsumptionMonth: float
    consumptionAlphaMonthKlg: float
    costTotalAlphaBs: float
    cubeChala: float
    UnitCostChalaBs: float
    costTotalChalaBs: float
    totalCharge: float
    fk_idOwner: int
    fk_idHorse: int


class TotalControlCreate(TotalControlBase):
    pass


class TotalControlUpdate(TotalControlBase):
    pass


class TotalControlInDBBase(TotalControlBase):
    idTotalControl: int
    created_at: datetime

    class Config:
        from_attributes = True


class TotalControl(TotalControlInDBBase):
    pass
