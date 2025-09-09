from datetime import datetime
from app.supabase_client import get_supabase
from app.schemas.owner_report_month import (
    OwnerReportMonthCreate,
    OwnerReportMonthUpdate,
)


def serialize_owner_report_month(report):
    """Convierte datetime a string para JSON"""
    data = report.model_dump(exclude_unset=True)
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    return data


async def get_owner_report_month(idOwnerReportMonth: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("owner_report_month")
        .select("*")
        .eq("idOwnerReportMonth", idOwnerReportMonth)
        .single()
        .execute()
    )
    return result.data if result.data else None


async def get_owner_report_months(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("owner_report_month")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data if result.data else []


async def create_owner_report_month(report: OwnerReportMonthCreate):
    supabase = await get_supabase()
    payload = serialize_owner_report_month(report)
    result = await supabase.table("owner_report_month").insert(payload).execute()
    return result.data[0] if result.data else None


async def update_owner_report_month(
    idOwnerReportMonth: int, report: OwnerReportMonthUpdate
):
    supabase = await get_supabase()
    payload = serialize_owner_report_month(report)
    result = (
        await supabase.table("owner_report_month")
        .update(payload)
        .eq("idOwnerReportMonth", idOwnerReportMonth)
        .execute()
    )
    return result.data[0] if result.data else None


async def delete_owner_report_month(idOwnerReportMonth: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("owner_report_month")
        .delete()
        .eq("idOwnerReportMonth", idOwnerReportMonth)
        .execute()
    )
    return result.data[0] if result.data else None
