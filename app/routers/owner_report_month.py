from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import owner_report_month as crud_report
from app.schemas import owner_report_month as schemas_report

router = APIRouter(prefix="/owner_report_month", tags=["Owner Report Month"])


@router.post("/", response_model=schemas_report.OwnerReportMonth, status_code=status.HTTP_201_CREATED)
async def create_owner_report_month(report_in: schemas_report.OwnerReportMonthCreate):
    try:
        report = await crud_report.create_owner_report_month(report_in)
        if not report:
            raise HTTPException(status_code=400, detail="No se pudo crear el reporte mensual.")
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el reporte: {str(e)}")


@router.get("/", response_model=List[schemas_report.OwnerReportMonth], status_code=status.HTTP_200_OK)
async def list_owner_report_months(skip: int = 0, limit: int = 100):
    try:
        reports = await crud_report.get_owner_report_months(skip=skip, limit=limit)
        return reports or []
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar reportes: {str(e)}")


@router.get("/{idOwnerReportMonth}", response_model=schemas_report.OwnerReportMonth, status_code=status.HTTP_200_OK)
async def get_owner_report_month(idOwnerReportMonth: int):
    try:
        report = await crud_report.get_owner_report_month(idOwnerReportMonth)
        if not report:
            raise HTTPException(status_code=404, detail="Reporte no encontrado.")
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el reporte: {str(e)}")


@router.put("/{idOwnerReportMonth}", response_model=schemas_report.OwnerReportMonth, status_code=status.HTTP_200_OK)
async def update_owner_report_month(idOwnerReportMonth: int, report_in: schemas_report.OwnerReportMonthUpdate):
    try:
        updated_report = await crud_report.update_owner_report_month(idOwnerReportMonth, report_in)
        if not updated_report:
            raise HTTPException(status_code=404, detail="No se encontró el reporte para actualizar.")
        return updated_report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el reporte: {str(e)}")


@router.delete("/{idOwnerReportMonth}", status_code=status.HTTP_200_OK)
async def delete_owner_report_month(idOwnerReportMonth: int):
    try:
        deleted_report = await crud_report.delete_owner_report_month(idOwnerReportMonth)
        if not deleted_report:
            raise HTTPException(status_code=404, detail="No se encontró el reporte para eliminar.")
        return {"message": "Reporte eliminado correctamente."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el reporte: {str(e)}")
