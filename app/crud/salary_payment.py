# app/crud/salary_payment.py
import base64
from datetime import datetime, date
from calendar import monthrange
from decimal import Decimal
from typing import Optional, Tuple

from app.supabase_client import get_supabase
from app.schemas.salary_payment import (
    SalaryPaymentCreate, SalaryPaymentUpdate,
)

# --------- Utilidades de serialización ----------
def _serialize_row(row: dict):
    """Convierte date/datetime a string y bytea->Base64; arma 'employee' con positionName."""
    if not row:
        return None
    data = {**row}

    # Convertir fechas/bytes
    for k, v in list(data.items()):
        if isinstance(v, (date, datetime)):
            data[k] = v.isoformat()
        elif isinstance(v, (bytes, bytearray)):
            data[k] = base64.b64encode(v).decode("utf-8")

    # Embedding de empleado con posición (depende del select embebido)
    emp = data.get("employee") or data.get("fk_idEmployee")
    if isinstance(emp, dict):
        pos = emp.get("employee_position") or emp.get("fk_idPositionEmployee")
        positionName = None
        if isinstance(pos, dict):
            positionName = pos.get("namePosition")
        data["employee"] = {
            "idEmployee": emp.get("idEmployee"),
            "fullName": emp.get("fullName"),
            "ci": emp.get("ci"),
            "salary": emp.get("salary"),
            "positionName": positionName,
        }
    return data

def _month_range(month_str: str) -> Tuple[date, date]:
    y, m = map(int, month_str.split("-"))
    start = date(y, m, 1)
    end = date(y, m, monthrange(y, m)[1])
    return start, end

# --------- CRUD ----------
async def create_salary_payment(payload: SalaryPaymentCreate):
    sb = await get_supabase()

    # Asegurar registrationDate por si no llega desde el front
    reg_dt: datetime = payload.registrationDate or datetime.utcnow()

    # Autocompletar paymentDate si viene PAID sin fecha
    payment_date = payload.paymentDate
    if (payload.state or "").upper() == "PAID" and payment_date is None:
        payment_date = reg_dt.date()

    to_insert = payload.model_dump(mode="json")
    to_insert["registrationDate"] = reg_dt.isoformat()
    to_insert["paymentDate"] = payment_date
    to_insert["updateDate"] = datetime.utcnow().isoformat()

    result = (
        await sb.table("salary_payment")
        .insert(to_insert)
        .select(
            "*, employee:fk_idEmployee (idEmployee, fullName, ci, salary, "
            "employee_position:fk_idPositionEmployee (namePosition))"
        )
        .single()
        .execute()
    )
    return _serialize_row(result.data) if result.data else None

async def get_salary_payment(idSalaryPayment: int):
    sb = await get_supabase()
    result = (
        await sb.table("salary_payment")
        .select(
            "*, employee:fk_idEmployee (idEmployee, fullName, ci, salary, "
            "employee_position:fk_idPositionEmployee (namePosition))"
        )
        .eq("idSalaryPayment", idSalaryPayment)
        .single()
        .execute()
    )
    return _serialize_row(result.data) if result.data else None

ALLOWED_ORDER = {"registrationDate", "paymentDate", "created_at", "amount"}

async def list_salary_payments(
    page: int = 1,
    limit: int = 10,
    employeeId: Optional[int] = None,
    state: Optional[str] = None,
    month: Optional[str] = None,           # YYYY-MM sobre registrationDate
    date_from: Optional[str] = None,       # ISO datetime
    date_to: Optional[str] = None,         # ISO datetime
    # search: Optional[str] = None,        # <- REMOVIDO: el front ya no lo envía
    orderBy: str = "registrationDate",
    order: str = "desc",
):
    sb = await get_supabase()
    q = (
        sb.table("salary_payment")
        .select(
            "*, employee:fk_idEmployee (idEmployee, fullName, ci, salary, "
            "employee_position:fk_idPositionEmployee (namePosition))",
            count="exact",
        )
    )

    if employeeId:
        q = q.eq("fk_idEmployee", employeeId)
    if state:
        q = q.eq("state", state)
    if month:
        start, end = _month_range(month)
        start_dt = f"{start.isoformat()}T00:00:00"
        end_dt = f"{end.isoformat()}T23:59:59"
        q = q.gte("registrationDate", start_dt).lte("registrationDate", end_dt)
    if date_from:
        q = q.gte("registrationDate", date_from)
    if date_to:
        q = q.lte("registrationDate", date_to)

    # Orden seguro
    ob = orderBy if orderBy in ALLOWED_ORDER else "registrationDate"
    desc = (order or "desc").lower() == "desc"
    q = q.order(ob, desc=desc)

    # Paginado (range es inclusivo)
    start_i = (page - 1) * limit
    end_i = start_i + limit - 1
    result = await q.range(start_i, end_i).execute()

    items = [_serialize_row(r) for r in (result.data or [])]
    total = result.count or 0
    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit
    }

async def update_salary_payment(idSalaryPayment: int, payload: SalaryPaymentUpdate):
    sb = await get_supabase()
    update_dict = payload.model_dump(mode="json", exclude_unset=True)

    # Regla: si cambia a PAID y no hay paymentDate, usar registrationDate
    new_state = update_dict.get("state")
    if new_state and new_state.upper() == "PAID" and "paymentDate" not in update_dict:
        # Preferir la registrationDate que llega en el update; si no, leer la actual
        reg = update_dict.get("registrationDate")
        if not reg:
            current = (
                await sb.table("salary_payment")
                .select("registrationDate")
                .eq("idSalaryPayment", idSalaryPayment)
                .single()
                .execute()
            )
            reg = current.data["registrationDate"] if current.data else None

        # reg puede ser str ISO o datetime
        if reg:
            if isinstance(reg, str):
                reg_date = reg.split("T")[0]
            else:
                reg_date = reg.date().isoformat()
            update_dict["paymentDate"] = reg_date

    update_dict["updateDate"] = datetime.utcnow().isoformat()

    result = (
        await sb.table("salary_payment")
        .update(update_dict)
        .eq("idSalaryPayment", idSalaryPayment)
        .select(
            "*, employee:fk_idEmployee (idEmployee, fullName, ci, salary, "
            "employee_position:fk_idPositionEmployee (namePosition))"
        )
        .single()
        .execute()
    )
    return _serialize_row(result.data) if result.data else None

async def delete_salary_payment(idSalaryPayment: int):
    sb = await get_supabase()
    result = (
        await sb.table("salary_payment")
        .delete()
        .eq("idSalaryPayment", idSalaryPayment)
        .select(
            "*, employee:fk_idEmployee (idEmployee, fullName, ci, salary, "
            "employee_position:fk_idPositionEmployee (namePosition))"
        )
        .single()
        .execute()
    )
    return _serialize_row(result.data) if result.data else None

# --------- Empleados para combos ---------
async def list_employees_for_payment(search: Optional[str] = None, limit: int = 20):
    sb = await get_supabase()
    q = sb.table("employee").select(
        "idEmployee, fullName, ci, salary, employee_position:fk_idPositionEmployee (namePosition)"
    )

    if search:
        if search.isdigit():
            q = q.eq("ci", int(search))
        else:
            q = q.ilike("fullName", f"%{search}%")

    q = q.order("fullName", desc=False).limit(limit)
    result = await q.execute()

    items = []
    for r in (result.data or []):
        pos = r.get("employee_position")
        items.append({
            "idEmployee": r["idEmployee"],
            "fullName": r["fullName"],
            "ci": r["ci"],
            "salary": r["salary"],
            "positionName": pos["namePosition"] if isinstance(pos, dict) else None
        })
    return items

# --------- Resumen mensual y asiento en expenses ---------
async def month_summary_total(
    month: str,
    state: Optional[str] = "PAID",
    employeeId: Optional[int] = None,
    usePaymentDate: bool = True,
):
    sb = await get_supabase()
    start, end = _month_range(month)
    if usePaymentDate:
        q = (sb.table("salary_payment").select("amount", count="exact")
             .gte("paymentDate", start.isoformat())
             .lte("paymentDate", end.isoformat()))
    else:
        start_dt = f"{start.isoformat()}T00:00:00"
        end_dt = f"{end.isoformat()}T23:59:59"
        q = (sb.table("salary_payment").select("amount", count="exact")
             .gte("registrationDate", start_dt)
             .lte("registrationDate", end_dt))

    if state:
        q = q.eq("state", state)
    if employeeId:
        q = q.eq("fk_idEmployee", employeeId)

    result = await q.limit(10000).execute()
    amounts = [Decimal(str(r["amount"])) for r in (result.data or [])]
    total = sum(amounts, Decimal("0"))
    count = result.count or len(amounts)
    return total, count

async def create_expense_from_month_total(
    month: str,
    total: Decimal,
    description: Optional[str] = None,
    expenseDate: Optional[date] = None,
):
    sb = await get_supabase()
    start, _ = _month_range(month)
    payload = {
        "date": (expenseDate or date.today()).isoformat(),
        "description": description or f"Planilla de sueldos {month}",
        "AmountBsCaptureType": str(total),
        "period": start.isoformat(),
    }
    res = await sb.table("expenses").insert(payload).select("*").single().execute()
    return res.data["idExpenses"] if res.data else None
