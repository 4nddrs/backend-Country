from datetime import date
from app.supabase_client import get_supabase
from app.schemas.medicine import MedicineCreate, MedicineUpdate
from app.scripts.notifier import notificar_medicamento


def serialize_medicine(medicine: dict):
    for field in ["boxExpirationDate"]:
        if medicine.get(field) and isinstance(medicine[field], date):
            medicine[field] = medicine[field].isoformat()
    return medicine


def calcular_estado_stock(stock: int, min_stock: int) -> str:
    if stock == 0:
        return "Agotado"
    elif stock < min_stock:
        return "Bajo"
    else:
        return "Disponible"


def calcular_estado_vencimiento(fecha_vencimiento: date) -> str:
    if not fecha_vencimiento:
        return "Vigente"
    hoy = date.today()
    if hoy > fecha_vencimiento:
        return "Vencido"
    elif (fecha_vencimiento - hoy).days <= 30:
        return "Por Vencer"
    return "Vigente"


async def get_medicine(idMedicine: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("medicine")
        .select("*")
        .eq("idMedicine", idMedicine)
        .single()
        .execute()
    )
    return serialize_medicine(result.data) if result.data else None


async def get_medicines(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("medicine")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [serialize_medicine(m) for m in result.data] if result.data else []


async def create_medicine(medicine: MedicineCreate):
    supabase = await get_supabase()
    medicine_dict = medicine.model_dump(mode="json")

    stock = medicine_dict.get("stock", 0)
    min_stock = medicine_dict.get("minStock", 0)
    fecha_venc = (
        date.fromisoformat(medicine_dict["boxExpirationDate"])
        if medicine_dict.get("boxExpirationDate")
        else None
    )

    # Calcular estados
    medicine_dict["stockStatus"] = calcular_estado_stock(stock, min_stock)
    medicine_dict["expiryStatus"] = calcular_estado_vencimiento(fecha_venc)

    # Si está agotado, se desactiva automáticamente
    if medicine_dict["stockStatus"].lower() == "agotado":
        medicine_dict["isActive"] = False
    else:
        medicine_dict["isActive"] = True

    result = await supabase.table("medicine").insert(medicine_dict).execute()
    return serialize_medicine(result.data[0]) if result.data else None


async def update_medicine(idMedicine: int, medicine: MedicineUpdate):
    from app.scripts.notifier import notificar_medicamento  # 👈 import dinámico

    supabase = await get_supabase()
    medicine_dict = medicine.model_dump(mode="json", exclude_unset=True)

    # Obtener datos actuales
    existing = (
        await supabase.table("medicine")
        .select("name, stock, minStock, boxExpirationDate")
        .eq("idMedicine", idMedicine)
        .single()
        .execute()
    )

    current_data = existing.data or {}
    nombre = current_data.get("name", "Desconocido")
    stock = medicine_dict.get("stock", current_data.get("stock", 0))
    min_stock = medicine_dict.get("minStock", current_data.get("minStock", 0))
    fecha_venc = (
        date.fromisoformat(
            medicine_dict.get("boxExpirationDate", current_data.get("boxExpirationDate"))
        )
        if (medicine_dict.get("boxExpirationDate") or current_data.get("boxExpirationDate"))
        else None
    )

    # Calcular estados
    medicine_dict["stockStatus"] = calcular_estado_stock(stock, min_stock)
    medicine_dict["expiryStatus"] = calcular_estado_vencimiento(fecha_venc)

    # Si está agotado, se desactiva automáticamente
    if medicine_dict["stockStatus"].lower() == "agotado":
        medicine_dict["isActive"] = False
    else:
        medicine_dict["isActive"] = True

    # Actualizar en Supabase
    result = (
        await supabase.table("medicine")
        .update(medicine_dict)
        .eq("idMedicine", idMedicine)
        .execute()
    )

    updated = serialize_medicine(result.data[0]) if result.data else None

    # 🚀 Enviar notificaciones si corresponde
    if updated:
        # 1️⃣ Stock bajo o agotado
        if stock <= min_stock:
            await notificar_medicamento(nombre, stock, min_stock, fecha_venc, motivo="stock")

        # 2️⃣ Medicamento próximo a vencer (7 días o menos)
        elif fecha_venc and (fecha_venc - date.today()).days <= 7:
            await notificar_medicamento(nombre, stock, min_stock, fecha_venc, motivo="vencimiento")

    return updated



async def delete_medicine(idMedicine: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("medicine")
        .delete()
        .eq("idMedicine", idMedicine)
        .execute()
    )
    return serialize_medicine(result.data[0]) if result.data else None
