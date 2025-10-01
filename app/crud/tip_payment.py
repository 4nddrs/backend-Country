import base64
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Dict, List, Optional

from app.supabase_client import get_supabase
from app.schemas.tip_payment import TipPaymentCreate, TipPaymentUpdate


def _serialize_value(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("utf-8")
    return value


def serialize_tip_payment(row: Dict[str, Any]) -> Dict[str, Any]:
    """Serializa un tip_payment respetando anidamientos de employee y employee_position."""
    if not row:
        return {}
    out: Dict[str, Any] = {}
    for k, v in row.items():
        if k == "employee" and isinstance(v, dict):
            emp: Dict[str, Any] = {}
            for ek, ev in v.items():
                if ek == "employee_position" and isinstance(ev, dict):
                    emp[ek] = {kk: _serialize_value(vv) for kk, vv in ev.items()}
                else:
                    emp[ek] = _serialize_value(ev)
            out[k] = emp
        else:
            out[k] = _serialize_value(v)
    return out


# ========= CRUD =========
async def get_tip_payment(idTipPayment: int) -> Optional[Dict[str, Any]]:
    supabase = await get_supabase()
    result = (
        await supabase.table("tip_payment")
        .select("""
            idTipPayment,
            created_at,
            amount,
            state,
            description,
            registrationDate,
            paymentDate,
            updateDate,
            fk_idEmployee,
            employee:fk_idEmployee (
                idEmployee,
                fullName,
                employee_position:fk_idPositionEmployee (
                    idPositionEmployee,
                    namePosition
                )
            )
        """)
        .eq("idTipPayment", idTipPayment)
        .single()
        .execute()
    )

    print("==== RESULT get_tip_payment ====")
    print(result.data)

    return serialize_tip_payment(result.data) if result.data else None


async def get_tip_payments(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    supabase = await get_supabase()
    result = (
        await supabase.table("tip_payment")
        .select("""
            idTipPayment,
            created_at,
            amount,
            state,
            description,
            registrationDate,
            paymentDate,
            updateDate,
            fk_idEmployee,
            employee:fk_idEmployee (
                idEmployee,
                fullName,
                employee_position:fk_idPositionEmployee (
                    idPositionEmployee,
                    namePosition
                )
            )
        """)
        .order("idTipPayment", desc=False)
        .range(skip, skip + limit - 1)
        .execute()
    )

    print("==== RESULT get_tip_payments ====")
    print(result.data)

    rows = result.data or []
    return [serialize_tip_payment(r) for r in rows]


async def create_tip_payment(payload: TipPaymentCreate) -> Optional[Dict[str, Any]]:
    supabase = await get_supabase()

    data = payload.model_dump(exclude_unset=True)
    data["registrationDate"] = datetime.utcnow().replace(tzinfo=None)
    data["updateDate"] = datetime.utcnow().replace(tzinfo=None)

    serialized = {k: _serialize_value(v) for k, v in data.items()}

    # 1️⃣ Insertar
    insert_result = await supabase.table("tip_payment").insert(serialized).execute()
    if not insert_result.data:
        return None

    new_id = insert_result.data[0]["idTipPayment"]

    # 2️⃣ Select con relaciones
    select_result = (
        await supabase.table("tip_payment")
        .select("""
            idTipPayment,
            created_at,
            amount,
            state,
            description,
            registrationDate,
            paymentDate,
            updateDate,
            fk_idEmployee,
            employee:fk_idEmployee (
                idEmployee,
                fullName,
                employee_position:fk_idPositionEmployee (
                    idPositionEmployee,
                    namePosition
                )
            )
        """)
        .eq("idTipPayment", new_id)
        .single()
        .execute()
    )

    return serialize_tip_payment(select_result.data) if select_result.data else None


async def update_tip_payment(
    idTipPayment: int, payload: TipPaymentUpdate
) -> Optional[Dict[str, Any]]:
    supabase = await get_supabase()

    data = payload.model_dump(exclude_unset=True)
    data["updateDate"] = datetime.utcnow().replace(tzinfo=None)

    serialized = {k: _serialize_value(v) for k, v in data.items()}

    # 1️⃣ Update
    update_result = (
        await supabase.table("tip_payment")
        .update(serialized)
        .eq("idTipPayment", idTipPayment)
        .execute()
    )
    if not update_result.data:
        return None

    # 2️⃣ Select actualizado con relaciones
    select_result = (
        await supabase.table("tip_payment")
        .select("""
            idTipPayment,
            created_at,
            amount,
            state,
            description,
            registrationDate,
            paymentDate,
            updateDate,
            fk_idEmployee,
            employee:fk_idEmployee (
                idEmployee,
                fullName,
                employee_position:fk_idPositionEmployee (
                    idPositionEmployee,
                    namePosition
                )
            )
        """)
        .eq("idTipPayment", idTipPayment)
        .single()
        .execute()
    )

    return serialize_tip_payment(select_result.data) if select_result.data else None


async def delete_tip_payment(idTipPayment: int) -> Optional[Dict[str, Any]]:
    supabase = await get_supabase()
    result = (
        await supabase.table("tip_payment")
        .delete()
        .eq("idTipPayment", idTipPayment)
        .execute()
    )
    return serialize_tip_payment(result.data[0]) if result.data else None
