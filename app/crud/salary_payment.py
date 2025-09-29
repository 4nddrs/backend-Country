import base64  # solo por simetría con otros módulos; no se usa aquí pero no afecta
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Dict, List, Optional

from app.supabase_client import get_supabase
from app.schemas.salary_payment import SalaryPaymentCreate, SalaryPaymentUpdate


def _serialize_value(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()  # datetime/date -> string
    if isinstance(value, Decimal):
        return float(value)       # Decimal -> float
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("utf-8")  # bytes -> Base64
    return value


def serialize_salary_payment(row: Dict[str, Any]) -> Dict[str, Any]:
    return {k: _serialize_value(v) for k, v in (row or {}).items()}


async def get_salary_payment(idSalaryPayment: int) -> Optional[Dict[str, Any]]:
    supabase = await get_supabase()
    result = (
        await supabase.table("salary_payment")
        .select("*")
        .eq("idSalaryPayment", idSalaryPayment)
        .single()
        .execute()
    )
    return serialize_salary_payment(result.data) if result.data else None


async def get_salary_payments(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    supabase = await get_supabase()
    result = (
        await supabase.table("salary_payment")
        .select("*")
        .order("idSalaryPayment", desc=False)
        .range(skip, skip + limit - 1)
        .execute()
    )
    rows = result.data or []
    return [serialize_salary_payment(r) for r in rows]


async def create_salary_payment(payload: SalaryPaymentCreate) -> Optional[Dict[str, Any]]:
    supabase = await get_supabase()

    data = payload.model_dump(exclude_unset=True)
    if "updateDate" not in data or data["updateDate"] is None:
        data["updateDate"] = datetime.utcnow().replace(tzinfo=None)

    # 🔥 Serializar valores antes de enviar
    serialized = {k: _serialize_value(v) for k, v in data.items()}

    result = await supabase.table("salary_payment").insert(serialized).execute()
    return serialize_salary_payment(result.data[0]) if result.data else None


async def update_salary_payment(
    idSalaryPayment: int, payload: SalaryPaymentUpdate
) -> Optional[Dict[str, Any]]:
    supabase = await get_supabase()

    data = payload.model_dump(exclude_unset=True)
    data["updateDate"] = datetime.utcnow().replace(tzinfo=None)

    # 🔥 Serializar valores antes de enviar
    serialized = {k: _serialize_value(v) for k, v in data.items()}

    result = (
        await supabase.table("salary_payment")
        .update(serialized)
        .eq("idSalaryPayment", idSalaryPayment)
        .execute()
    )
    return serialize_salary_payment(result.data[0]) if result.data else None


async def delete_salary_payment(idSalaryPayment: int) -> Optional[Dict[str, Any]]:
    supabase = await get_supabase()
    result = (
        await supabase.table("salary_payment")
        .delete()
        .eq("idSalaryPayment", idSalaryPayment)
        .execute()
    )
    return serialize_salary_payment(result.data[0]) if result.data else None
