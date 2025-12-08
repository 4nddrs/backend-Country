import asyncio
from datetime import date, datetime, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.supabase_client import get_supabase

router = APIRouter(tags=["dashboard"])

CACHE_TTL_SECONDS = 30
_dashboard_cache: Dict[str, Any] = {"data": None, "expires_at": datetime.min}
_cache_lock = asyncio.Lock()


def _parse_to_date(value) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None
    return None


def _month_start(dt: date) -> date:
    return dt.replace(day=1)


def _add_months(dt: date, months: int) -> date:
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    return date(year, month, 1)

def _normalize_status(value: str | None) -> str:
    text = (value or "").strip().lower()
    if "cancel" in text:
        return "Cancelada"
    if "complet" in text or "finaliz" in text:
        return "Completada"
    if "progr" in text or "proceso" in text:
        return "En progreso"
    return "Pendiente"


async def _tasks_summary(supabase) -> List[Dict[str, Any]]:
    res = await supabase.table("task").select("taskStatus").execute()
    counts: Dict[str, int] = {}
    for item in res.data or []:
        status = _normalize_status(item.get("taskStatus"))
        counts[status] = counts.get(status, 0) + 1
    return [{"status": status, "count": count} for status, count in counts.items()]


async def _recent_attentions(supabase, errors: List[str], limit: int = 5) -> List[Dict[str, Any]]:
    """
    Obtiene atenciones recientes con joins manuales para evitar errores de sintaxis en Supabase.
    """
    try:
        attentions_res = (
            await supabase.table("attention_horse")
            .select("idAttentionHorse,date,description,cost,fk_idHorse,fk_idEmployee")
            .order("date", desc=True)
            .limit(limit)
            .execute()
        )
    except Exception as exc:
        errors.append(f"attention_horse: {exc}")
        return []

    try:
        horses_res = await supabase.table("horse").select("idHorse,horseName").execute()
        employees_res = await supabase.table("employee").select("idEmployee,fullName").execute()
    except Exception as exc:
        errors.append(f"horse/employee: {exc}")
        return []

    horse_map = {h.get("idHorse"): h.get("horseName") for h in horses_res.data or []}
    employee_map = {e.get("idEmployee"): e.get("fullName") for e in employees_res.data or []}

    out = []
    for item in attentions_res.data or []:
        out.append(
            {
                "idAttentionHorse": item.get("idAttentionHorse"),
                "date": item.get("date"),
                "description": item.get("description"),
                "cost": float(item.get("cost") or 0),
                "horseName": horse_map.get(item.get("fk_idHorse"), "Desconocido"),
                "employeeName": employee_map.get(item.get("fk_idEmployee"), "Desconocido"),
            }
        )
    return out


async def _fetch_financial_records(
    supabase, table: str, date_field: str, amount_field: str, start: date
) -> List[Dict[str, Any]]:
    res = (
        await supabase.table(table)
        .select(f"{date_field},{amount_field}")
        .gte(date_field, start.isoformat())
        .execute()
    )
    return res.data or []


def _group_by_month(records: List[Dict[str, Any]], date_field: str, amount_field: str) -> Dict[str, float]:
    grouped: Dict[str, float] = {}
    for item in records:
        d = _parse_to_date(item.get(date_field))
        if not d:
            continue
        key = f"{d.year:04d}-{d.month:02d}"
        amount = item.get(amount_field)
        # Fallbacks por si cambia el nombre del campo
        if amount is None:
            amount = item.get("AmountBsCaptureType") or item.get("amount") or item.get("Amount") or item.get("totalAmount")
        grouped[key] = grouped.get(key, 0.0) + float(amount or 0.0)
    return grouped


def _group_by_day(records: List[Dict[str, Any]], date_field: str, amount_field: str, kind: str) -> Dict[str, Dict[str, float]]:
    grouped: Dict[str, Dict[str, float]] = {}
    for item in records:
        d = _parse_to_date(item.get(date_field))
        if not d:
            continue
        key = d.isoformat()
        amount = item.get(amount_field)
        if amount is None:
            amount = item.get("AmountBsCaptureType") or item.get("amount") or item.get("Amount") or item.get("totalAmount")
        amount_value = float(amount or 0.0)
        entry = grouped.get(key, {"income": 0.0, "expenses": 0.0})
        grouped[key] = entry
        if kind == "income":
            entry["income"] += amount_value
        else:
            entry["expenses"] += amount_value
    return grouped


async def _compute_dashboard() -> Dict[str, Any]:
    supabase = await get_supabase()
    errors: List[str] = []
    today = date.today()
    current_month_start = _month_start(today)
    oldest_month_start = _add_months(current_month_start, -11)

    async def safe_query(name: str, coro):
        try:
            res = await coro
            if getattr(res, "error", None):
                errors.append(f"{name}: {res.error}")
                return []
            return res.data or []
        except Exception as exc:
            errors.append(f"{name}: {exc}")
            return []

    horses_task = asyncio.create_task(safe_query("horses", supabase.table("horse").select("idHorse,state,stateSchool").execute()))
    employees_task = asyncio.create_task(safe_query("employees", supabase.table("employee").select("idEmployee,status").execute()))
    owners_task = asyncio.create_task(safe_query("owners", supabase.table("owner").select("idOwner").execute()))
    tasks_task = asyncio.create_task(safe_query("tasks", supabase.table("task").select("taskStatus").execute()))
    attentions_task = asyncio.create_task(
        safe_query(
            "attention_horse",
            supabase.table("attention_horse")
            .select("idAttentionHorse,date,description,cost,fk_idHorse,fk_idEmployee")
            .order("date", desc=True)
            .limit(8)
            .execute(),
        )
    )
    incomes_task = asyncio.create_task(
        safe_query(
            "income",
            supabase.table("income")
            .select("date,amountBsCaptureType")
            .gte("date", oldest_month_start.isoformat())
            .execute(),
        )
    )
    expenses_task = asyncio.create_task(
        safe_query(
            "expenses",
            supabase.table("expenses")
            .select("date,AmountBsCaptureType")
            .gte("date", oldest_month_start.isoformat())
            .execute(),
        )
    )

    horses = await horses_task
    employees = await employees_task
    owners = await owners_task
    tasks_raw = await tasks_task
    _ = await attentions_task  # fetched separately below
    incomes = await incomes_task
    expenses = await expenses_task

    horses_total = len(horses)
    horses_active = len([h for h in horses if (h.get("state") or "").upper() == "ACTIVO"])
    horses_school = len([h for h in horses if h.get("stateSchool") is True])

    employees_total = len(employees)
    employees_active = len([e for e in employees if e.get("status") is True])

    owners_total = len(owners)

    # Resumen de tareas
    counts: Dict[str, int] = {}
    for item in tasks_raw:
        status = item.get("taskStatus") or "SIN_ESTADO"
        counts[status] = counts.get(status, 0) + 1
    tasks_summary = [{"status": status, "count": count} for status, count in counts.items()]

    recent_attentions = await _recent_attentions(supabase, errors, limit=8)

    incomes_by_month = _group_by_month(incomes, "date", "amountBsCaptureType")
    expenses_by_month = _group_by_month(expenses, "date", "AmountBsCaptureType")

    # Agrupar por día para gráficas detalladas
    incomes_by_day = _group_by_day(incomes, "date", "amountBsCaptureType", "income")
    expenses_by_day = _group_by_day(expenses, "date", "AmountBsCaptureType", "expenses")
    daily_keys = sorted(set(list(incomes_by_day.keys()) + list(expenses_by_day.keys())))
    daily_financials = []
    for day in daily_keys:
        income_val = incomes_by_day.get(day, {}).get("income", 0.0)
        expense_val = expenses_by_day.get(day, {}).get("expenses", 0.0)
        daily_financials.append(
            {
                "date": day,
                "income": round(income_val, 2),
                "expenses": round(expense_val, 2),
            }
        )

    months = [_add_months(current_month_start, offset) for offset in range(-11, 1)]
    monthly_financials = []
    for m in months:
        label = f"{m.year:04d}-{m.month:02d}"
        inc = round(incomes_by_month.get(label, 0.0), 2)
        exp = round(expenses_by_month.get(label, 0.0), 2)
        monthly_financials.append(
            {
                "month": label,
                "income": inc,
                "expenses": exp,
                "net": round(inc - exp, 2),
            }
        )

    current_label = f"{current_month_start.year:04d}-{current_month_start.month:02d}"
    income_this_month = incomes_by_month.get(current_label, 0.0)
    expenses_this_month = expenses_by_month.get(current_label, 0.0)

    pending_tasks = 0
    in_progress_tasks = 0
    completed_tasks = 0
    for item in tasks_summary:
        status = item.get("status", "")
        if status == "Pendiente":
            pending_tasks += item.get("count", 0)
        elif status == "En progreso":
            in_progress_tasks += item.get("count", 0)
        elif status == "Completada":
            completed_tasks += item.get("count", 0)

    return {
        "stats": {
            "totalHorses": horses_total,
            "activeHorses": horses_active,
            "schoolHorses": horses_school,
            "totalEmployees": employees_total,
            "activeEmployees": employees_active,
            "totalOwners": owners_total,
            "pendingTasks": pending_tasks,
            "completedTasks": completed_tasks,
            "monthlyIncome": round(income_this_month, 2),
            "monthlyExpenses": round(expenses_this_month, 2),
            "netBalance": round(income_this_month - expenses_this_month, 2),
        },
        "tasksSummary": tasks_summary,
        "recentAttentions": recent_attentions,
        "monthlyFinancials": [
            {"month": m["month"], "income": m["income"], "expenses": m["expenses"]}
            for m in monthly_financials
        ],
        "dailyFinancials": daily_financials,
        "errors": errors,
    }


async def _get_cached_dashboard() -> Dict[str, Any] | None:
    now = datetime.utcnow()
    if _dashboard_cache["data"] and now < _dashboard_cache["expires_at"]:
        return _dashboard_cache["data"]
    return None


async def _set_cache(data: Dict[str, Any]):
    _dashboard_cache["data"] = data
    _dashboard_cache["expires_at"] = datetime.utcnow() + timedelta(seconds=CACHE_TTL_SECONDS)


@router.get("/dashboard")
async def get_dashboard():
    cached = await _get_cached_dashboard()
    if cached:
        return cached

    async with _cache_lock:
        cached = await _get_cached_dashboard()
        if cached:
            return cached

        try:
            data = await _compute_dashboard()
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Error al construir el dashboard: {exc}") from exc

        await _set_cache(data)
        return data
