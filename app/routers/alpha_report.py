from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Any
from app.schemas.alpha_report import ConsumptionReportOut
from app.crud.alpha_report import (
    list_foods, list_periods_by_food, build_consumption_report, report_all_months_all_foods
)

router = APIRouter(prefix="/alpha_consumption_control", tags=["alpha_consumption_control"])

# Combo de alimentos (con búsqueda opcional)
@router.get("/foods")
async def foods(q: Optional[str] = Query(None, description="Filtro por nombre")):
    try:
        return await list_foods(q=q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Periodos disponibles según alimento (si no mandas food_id => todos)
@router.get("/periods", response_model=List[str])
async def periods(food_id: Optional[int] = Query(None)):
    try:
        return await list_periods_by_food(food_id=food_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Reporte mensual (opcional: filtrado por alimento)
@router.get("/consumption", response_model=ConsumptionReportOut)
async def consumption(period_month: str = Query(..., example="2025-06"),
                      food_id: Optional[int] = Query(None)):
    try:
        return await build_consumption_report(period_month, food_id=food_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# (Opcional) todos los meses, todos los alimentos
@router.get("/consumption/all")
async def consumption_all():
    try:
        return await report_all_months_all_foods()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
