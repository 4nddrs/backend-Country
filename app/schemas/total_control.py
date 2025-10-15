from pydantic import BaseModel
from datetime import datetime , date
from typing import Optional


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
    box: Optional[float] = None
    section: Optional[float] = None
    basket: Optional[float] = None
    period: date


class TotalControlCreate(TotalControlBase):
    pass


class TotalControlUpdate(BaseModel):
    toCaballerizo: Optional[float] = None
    vaccines: Optional[float] = None
    anemia: Optional[float] = None
    deworming: Optional[float] = None
    consumptionAlfaDiaKlg: Optional[float] = None
    costAlfaBs: Optional[float] = None
    daysConsumptionMonth: Optional[float] = None
    consumptionAlphaMonthKlg: Optional[float] = None
    costTotalAlphaBs: Optional[float] = None
    cubeChala: Optional[float] = None
    UnitCostChalaBs: Optional[float] = None
    costTotalChalaBs: Optional[float] = None
    totalCharge: Optional[float] = None
    fk_idOwner: Optional[int] = None
    fk_idHorse: Optional[int] = None
    box: Optional[float] = None
    section: Optional[float] = None
    basket: Optional[float] = None
    period: Optional[date] = None


class TotalControlInDBBase(TotalControlBase):
    idTotalControl: int
    created_at: datetime

    class Config:
        from_attributes = True


class TotalControl(TotalControlInDBBase):
    pass
