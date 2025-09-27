from datetime import datetime, date
from decimal import Decimal
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

from app.supabase_client import get_supabase
from app.schemas.salary_payment import (
    SalaryPaymentCreate, SalaryPaymentUpdate,
    SalaryMonthSummaryOut, SalaryMonthSummaryItem,
    ClosePayrollRequest, ClosePayrollResult
)

TABLE = "salary_payment"
EMP_TABLE = "employee"
EXP_TABLE = "expenses"

def _month_bounds(period_month: str) -> Tuple[date, date, str]:
    y, m = map(int, period_month.split("-"))
    start = date(y, m, 1)
    # siguiente mes
    end = date(y + (m // 12), (m % 12) + 1, 1)
    return start, end, f"{y:04d}-{m:02d}"

# ===== CRUD básico =====
async def get_salary_payment(id_salary_payment: int):
    sb = await get_supabase()
    res = (await sb.table(TABLE).select("*")
           .eq("idSalaryPayment", id_salary_payment).single().execute())
    return res.data if res.data else None

async def get_salary_payments(skip: int = 0, limit: int = 100):
    sb = await get_supabase()
    res = (await sb.table(TABLE).select("*")
           .order("idSalaryPayment", desc=True)
           .range(skip, skip + limit - 1).execute())
    return res.data or []

async def create_salary_payment(data_in: SalaryPaymentCreate):
    sb = await get_supabase()
    payload = data_in.model_dump(mode="json")
    payload["updateDate"] = datetime.utcnow().isoformat(timespec="seconds")
    res = await sb.table(TABLE).insert(payload).execute()
    return res.data[0] if res.data else None

async def update_salary_payment(id_salary_payment: int, data_in: SalaryPaymentUpdate):
    sb = await get_supabase()
    payload = data_in.model_dump(mode="json", exclude_unset=True)
    if not payload.get("updateDate"):
        payload["updateDate"] = datetime.utcnow().isoformat(timespec="seconds")
    res = (await sb.table(TABLE).update(payload)
           .eq("idSalaryPayment", id_salary_payment).execute())
    return res.data[0] if res.data else None

async def delete_salary_payment(id_salary_payment: int):
    sb = await get_supabase()
    res = (await sb.table(TABLE).delete()
           .eq("idSalaryPayment", id_salary_payment).execute())
    return res.data[0] if res.data else None


# ====== Resumen mensual ======
async def salary_month_summary(period_month: str) -> SalaryMonthSummaryOut:
    start, end, tag = _month_bounds(period_month)
    sb = await get_supabase()

    # obtén pagos del mes (por registrationDate)
    pay = (await sb.table(TABLE).select(
            "idSalaryPayment,amount,fk_idEmployee,registrationDate,state")
           .gte("registrationDate", start.isoformat())
           .lt("registrationDate", end.isoformat())
           .execute()).data or []

    # agrupar por empleado
    sums: Dict[int, Dict[str, Decimal | int]] = defaultdict(lambda: {
        "total": Decimal("0"),
        "count": 0
    })
    emp_ids = set()
    for p in pay:
        eid = int(p["fk_idEmployee"])
        emp_ids.add(eid)
        amt = Decimal(str(p.get("amount") or "0"))
        sums[eid]["total"] += amt
        sums[eid]["count"] += 1

    # nombres de empleados
    names: Dict[int, str] = {}
    if emp_ids:
        emp_res = (await sb.table(EMP_TABLE)
                   .select("idEmployee,fullName")
                   .in_("idEmployee", list(emp_ids)).execute()).data or []
        for e in emp_res:
            names[int(e["idEmployee"])] = e.get("fullName", str(e["idEmployee"]))

    items: List[SalaryMonthSummaryItem] = []
    grand = Decimal("0")
    total_records = 0
    for eid, ag in sums.items():
        total = Decimal(ag["total"])
        count = int(ag["count"])
        grand += total
        total_records += count
        items.append(SalaryMonthSummaryItem(
            fk_idEmployee=eid,
            employee_name=names.get(eid, str(eid)),
            total_amount=total,
            count_payments=count
        ))

    # ordenar por total descendente
    items.sort(key=lambda x: x.total_amount, reverse=True)

    return SalaryMonthSummaryOut(
        period_month=tag,
        items=items,
        grand_total=grand,
        total_records=total_records
    )


# ====== Cerrar nómina (crear expense + marcar PAGADO) ======
async def close_month_payroll(req: ClosePayrollRequest) -> ClosePayrollResult:
    start, end, tag = _month_bounds(req.period_month)
    sb = await get_supabase()

    # pagos del mes sin PAGAR (o todos? tomamos los no pagados)
    pay_q = (await sb.table(TABLE).select(
                "idSalaryPayment,amount")
             .gte("registrationDate", start.isoformat())
             .lt("registrationDate", end.isoformat())
             .neq("state", "PAGADO")
             .execute())
    payments = pay_q.data or []
    if not payments:
        return ClosePayrollResult(
            period_month=tag, updated_count=0, total_amount=Decimal("0"), expense_id=None
        )

    total = sum(Decimal(str(p["amount"])) for p in payments)
    now_iso = datetime.utcnow().isoformat(timespec="seconds")

    # 1) marcar pagos como PAGADO
    ids = [p["idSalaryPayment"] for p in payments]
    # Supabase no admite update masivo con lista directamente en algunos clientes;
    # hacemos in() + update
    _ = (await sb.table(TABLE).update({
            "state": "PAGADO",
            "paymentDate": (req.expense_date or date.today()).isoformat(),
            "updateDate": now_iso
         }).in_("idSalaryPayment", ids).execute())

    expense_id: Optional[int] = None
    if req.create_expense:
        desc = req.expense_description or f"Nómina mes {tag}"
        exp_payload = {
            "date": (req.expense_date or date.today()).isoformat(),
            "description": desc,
            "AmountBsCaptureType": str(total),
            "period": start.isoformat()
        }
        exp_ins = await sb.table(EXP_TABLE).insert(exp_payload).execute()
        if exp_ins.data:
            expense_id = exp_ins.data[0]["idExpenses"]

    return ClosePayrollResult(
        period_month=tag,
        updated_count=len(ids),
        total_amount=total,
        expense_id=expense_id
    )
