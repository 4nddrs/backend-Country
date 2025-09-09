from datetime import date
from app.supabase_client import get_supabase
from app.schemas.employee_absence import EmployeeAbsenceCreate, EmployeeAbsenceUpdate


def serialize_employee_absence(absence: dict):
    """Convierte campos de fecha a ISO string."""
    for field in ["startDate", "endDate"]:
        if absence.get(field) and isinstance(absence[field], date):
            absence[field] = absence[field].isoformat()
    return absence


async def get_employee_absence(idEmployeeAbsence: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("employee_absence")
        .select("*")
        .eq("idEmployeeAbsence", idEmployeeAbsence)
        .single()
        .execute()
    )
    return serialize_employee_absence(result.data) if result.data else None


async def get_employee_absences(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("employee_absence")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [serialize_employee_absence(a) for a in result.data] if result.data else []


async def create_employee_absence(absence: EmployeeAbsenceCreate):
    supabase = await get_supabase()
    absence_dict = absence.model_dump(mode="json")
    result = await supabase.table("employee_absence").insert(absence_dict).execute()
    return serialize_employee_absence(result.data[0]) if result.data else None


async def update_employee_absence(
    idEmployeeAbsence: int, absence: EmployeeAbsenceUpdate
):
    supabase = await get_supabase()
    absence_dict = absence.model_dump(mode="json", exclude_unset=True)
    result = (
        await supabase.table("employee_absence")
        .update(absence_dict)
        .eq("idEmployeeAbsence", idEmployeeAbsence)
        .execute()
    )
    return serialize_employee_absence(result.data[0]) if result.data else None


async def delete_employee_absence(idEmployeeAbsence: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("employee_absence")
        .delete()
        .eq("idEmployeeAbsence", idEmployeeAbsence)
        .execute()
    )
    return serialize_employee_absence(result.data[0]) if result.data else None
