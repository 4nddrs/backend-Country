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

# --------- helpers ----------
def _serialize_row(row: dict):
    """Convierte fechas a ISO y arma employee.positionName desde la relación."""
    if not row:
        return None
    data = dict(row)

    for k, v in list(data.items()):
        if isinstance(v, (datetime, date)):
            data[k] = v.isoformat()
        elif isinstance(v, (bytes, bytearray)):
            data[k] = base64.b64encode(v).decode("utf-8")

    emp = data.get("employee")
    if isinstance(emp, dict):
        pos = emp.get("employee_position") or emp.get("fk_idPositionEmployee")
        positionName = pos.get("namePosition") if isinstance(pos, dict) else None
        data["employee"] = {
            "idEmployee": emp.get("idEmployee"),
            "fullName": emp.get("fullName"),
            "ci": emp.get("ci"),
            "salary": emp.get("salary"),
            "positionName": positionName,
        }
    return data

def _month_range(month_str: str):
    y, m = map(int, month_str.split("-"))
    start = date(y, m, 1)
    end = date(y, m, monthrange(y, m)[1])
    return start, end

# --------- CRUD ----------
async def create_salary_payment(payload: SalaryPaymentCreate):
    sb = await get_supabase()

    # Backend fija la fecha de registro
    reg_dt = datetime.utcnow()

    # Si viene PAID sin paymentDate, usar la fecha del registro
    payment_date = payload.paymentDate
    if (payload.state or "").upper() == "PAID" and payment_date is None:
        payment_date = reg_dt.date()

    to_insert = payload.model_dump(mode="json")
    to_insert["registrationDate"] = reg_dt.isoformat()
    to_insert["paymentDate"] = payment_date
    to_insert["updateDate"] = reg_dt.isoformat()

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
    month: Optional[str] = None,  # YYYY-MM (sobre registrationDate)
    orderBy: str = "registrationDate",
    order: str = "desc",
):
    sb = await get_supabase()
    q = sb.table("salary_payment").select(
        "*, employee:fk_idEmployee (idEmployee, fullName, ci, salary, "
        "employee_position:fk_idPositionEmployee (namePosition))",
        count="exact",
    )

    if employeeId:
        q = q.eq("fk_idEmployee", employeeId)
    if state:
        q = q.eq("state", state)
    if month:
        start, end = _month_range(month)
        q = q.gte("registrationDate", f"{start.isoformat()}T00:00:00") \
             .lte("registrationDate", f"{end.isoformat()}T23:59:59")

    # Orden seguro
    ob = orderBy if orderBy in ALLOWED_ORDER else "registrationDate"
    q = q.order(ob, desc=(order.lower() == "desc"))

    # Paginado
    start_i = (page - 1) * limit
    end_i = start_i + limit - 1
    result = await q.range(start_i, end_i).execute()

    items = [_serialize_row(r) for r in (result.data or [])]
    total = result.count or 0
    return {"items": items, "total": total, "page": page, "limit": limit}

async def update_salary_payment(idSalaryPayment: int, payload: SalaryPaymentUpdate):
    sb = await get_supabase()
    update_dict = payload.model_dump(mode="json", exclude_unset=True)

    # Si pasa a PAID y no envían paymentDate, usar registrationDate (la nueva o la actual)
    new_state = update_dict.get("state")
    if new_state and new_state.upper() == "PAID" and "paymentDate" not in update_dict:
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

# --------- Empleados para el combo del front ----------
async def list_employees_for_payment(search: Optional[str] = None, limit: int = 50):
    sb = await get_supabase()
    q = sb.table("employee").select(
        "idEmployee, fullName, ci, salary, employee_position:fk_idPositionEmployee (namePosition)"
    )
    if search:
        if search.isdigit():
            q = q.eq("ci", int(search))
        else:
            q = q.ilike("fullName", f"%{search}%")

    q = q.order("fullName").limit(limit)
    result = await q.execute()

    items = []
    for r in (result.data or []):
        pos = r.get("employee_position")
        items.append({
            "idEmployee": r["idEmployee"],
            "fullName": r["fullName"],
            "ci": r["ci"],
            "salary": r["salary"],
            "positionName": pos["namePosition"] if isinstance(pos, dict) else None,
        })
    return items
