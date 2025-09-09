from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import owner_report_month as crud_report
from app.schemas import owner_report_month as schemas_report

router = APIRouter(prefix="/owner_report_month", tags=["owner_report_month"])


@router.post(
    "/",
    response_model=schemas_report.OwnerReportMonth,
    status_code=status.HTTP_201_CREATED,
)
async def create_owner_report_month(report_in: schemas_report.OwnerReportMonthCreate):
    report = await crud_report.create_owner_report_month(report_in)
    if not report:
        raise HTTPException(status_code=400, detail="Report could not be created")
    return report


@router.get("/", response_model=List[schemas_report.OwnerReportMonth])
async def list_owner_report_months(skip: int = 0, limit: int = 100):
    return await crud_report.get_owner_report_months(skip=skip, limit=limit)


@router.get("/{idOwnerReportMonth}", response_model=schemas_report.OwnerReportMonth)
async def get_owner_report_month(idOwnerReportMonth: int):
    report = await crud_report.get_owner_report_month(idOwnerReportMonth)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.put("/{idOwnerReportMonth}", response_model=schemas_report.OwnerReportMonth)
async def update_owner_report_month(
    idOwnerReportMonth: int, report_in: schemas_report.OwnerReportMonthUpdate
):
    updated_report = await crud_report.update_owner_report_month(
        idOwnerReportMonth, report_in
    )
    if not updated_report:
        raise HTTPException(status_code=404, detail="Report not found")
    return updated_report


@router.delete("/{idOwnerReportMonth}", response_model=schemas_report.OwnerReportMonth)
async def delete_owner_report_month(idOwnerReportMonth: int):
    deleted_report = await crud_report.delete_owner_report_month(idOwnerReportMonth)
    if not deleted_report:
        raise HTTPException(status_code=404, detail="Report not found")
    return deleted_report
