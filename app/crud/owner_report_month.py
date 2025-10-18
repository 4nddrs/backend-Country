from datetime import datetime , date
from app.supabase_client import get_supabase
from app.schemas.owner_report_month import OwnerReportMonthCreate, OwnerReportMonthUpdate


def serialize_owner_report_month(report):
    data = report.model_dump(exclude_unset=True, exclude={"horses_report"})
    for key, value in data.items():
        if isinstance(value, (datetime, date)):  
            data[key] = value.isoformat()
    return data


async def get_owner_report_month(idOwnerReportMonth: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("owner_report_month")
        .select("""
            *,
            owner:fk_idOwner (
                idOwner,
                name,
                "FirstName",
                "SecondName",
                horses:horse (
                    idHorse,
                    horseName,
                    box,
                    section
                )
            ),
            horses_report:horse_report_month (
                idHorseReportMonth,
                fk_idHorse,
                days,
                alphaKg,
                created_at
            )
        """)
        .eq("idOwnerReportMonth", idOwnerReportMonth)
        .single()
        .execute()
    )

    data = result.data
    if not data:
        return None

    owner = data.get("owner")
    if owner and "horses" in owner:
        owner["horses"] = [
            h for h in owner["horses"]
            if h.get("box") is True and h.get("section") is True
        ]

    return data


async def get_owner_report_months(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("owner_report_month")
        .select("""
            *,
            owner:fk_idOwner (
                idOwner,
                name,
                "FirstName",
                "SecondName"
            ),
            horses_report:horse_report_month (
                idHorseReportMonth,
                fk_idHorse,
                days,
                alphaKg,
                created_at
            )
        """)
        .order("created_at", desc=True)
        .range(skip, skip + limit - 1)
        .execute()
    )
    return result.data or []


async def create_owner_report_month(report: OwnerReportMonthCreate):
    supabase = await get_supabase()
    payload = serialize_owner_report_month(report)
    horses_report = report.horses_report or []

    result_report = await supabase.table("owner_report_month").insert(payload).execute()
    if not result_report.data:
        return None

    new_report = result_report.data[0]
    id_report = new_report["idOwnerReportMonth"]

    if horses_report:
        horse_payloads = []
        for horse in horses_report:
            horse_payloads.append({
                "fk_idOwnerReportMonth": id_report,
                "fk_idHorse": horse.fk_idHorse,
                "days": horse.days,
                "alphaKg": horse.alphaKg,
            })
        await supabase.table("horse_report_month").insert(horse_payloads).execute()

    final_result = (
        await supabase.table("owner_report_month")
        .select("""
            *,
            horses_report:horse_report_month (
                idHorseReportMonth,
                fk_idHorse,
                days,
                alphaKg,
                created_at
            )
        """)
        .eq("idOwnerReportMonth", id_report)
        .single()
        .execute()
    )

    return final_result.data


async def update_owner_report_month(idOwnerReportMonth: int, report: OwnerReportMonthUpdate):
    supabase = await get_supabase()
    payload = serialize_owner_report_month(report)
    horses_report = getattr(report, "horses_report", None)

    result = (
        await supabase.table("owner_report_month")
        .update(payload)
        .eq("idOwnerReportMonth", idOwnerReportMonth)
        .execute()
    )

    if not result.data:
        return None

    if horses_report is not None:
        await supabase.table("horse_report_month") \
            .delete() \
            .eq("fk_idOwnerReportMonth", idOwnerReportMonth) \
            .execute()

        if len(horses_report) > 0:
            horse_payloads = []
            for horse in horses_report:
                horse_payloads.append({
                    "fk_idOwnerReportMonth": idOwnerReportMonth,
                    "fk_idHorse": horse.fk_idHorse,
                    "days": horse.days,
                    "alphaKg": horse.alphaKg,
                })
            await supabase.table("horse_report_month").insert(horse_payloads).execute()

    final_result = (
        await supabase.table("owner_report_month")
        .select("""
            *,
            horses_report:horse_report_month (
                idHorseReportMonth,
                fk_idHorse,
                days,
                alphaKg,
                created_at
            )
        """)
        .eq("idOwnerReportMonth", idOwnerReportMonth)
        .single()
        .execute()
    )

    return final_result.data


async def delete_owner_report_month(idOwnerReportMonth: int):
    supabase = await get_supabase()

    await supabase.table("horse_report_month") \
        .delete() \
        .eq("fk_idOwnerReportMonth", idOwnerReportMonth) \
        .execute()

    result = (
        await supabase.table("owner_report_month")
        .delete()
        .eq("idOwnerReportMonth", idOwnerReportMonth)
        .execute()
    )

    return result.data[0] if result.data else None
