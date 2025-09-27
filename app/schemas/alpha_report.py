from pydantic import BaseModel, Field
from typing import List, Optional

class ConsumptionReportQuery(BaseModel):
    period_month: str = Field(..., example="2025-06")  # YYYY-MM
    food_id: Optional[int] = None  # si va vacío => todos los alimentos

class ConsumptionReportRow(BaseModel):
    horse_id: int
    horse_name: str
    owner_id: int
    owner_name: str
    period: str                   # YYYY-MM
    consumptionKlg: float         # suma mensual (filtrado por food si aplica)
    daysConsumptionMonth: float   # suma mensual
    klgMes: float                 # consumoKlg * días (agregado)
    stateSchool: bool             # 👈 NUEVO: True si el caballo pertenece a escuela
    # state: Optional[str] = None # (opcional) ACTIVO | AUSENTE | FALLECIDO

class ConsumptionReportSummary(BaseModel):
    comen: int
    no_comen: int
    caballos_escuela: int         # se calcula con los rows.stateSchool
    total_caballos: int
    total_klg: float
    total_klg_mes: float

class ConsumptionReportOut(BaseModel):
    period_month: str
    food_id: Optional[int] = None
    food_name: Optional[str] = None
    rows: List[ConsumptionReportRow]
    summary: ConsumptionReportSummary
