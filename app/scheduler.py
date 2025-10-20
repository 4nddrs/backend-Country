from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from app.supabase_client import get_supabase
import asyncio
import requests

# Configuración del bot
BOT_TOKEN = "8225256599:AAEWeT5H-LP069Gz631-1qBgDOyn6MwS5Zs"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

scheduler = BackgroundScheduler()

async def verificar_medicamentos():
    supabase = await get_supabase()
    hoy = date.today()

    # 1️⃣ Obtener todos los medicamentos activos
    result = await supabase.table("medicine").select("*").eq("isActive", True).execute()
    medicines = result.data or []

    if not medicines:
        print("📦 No hay medicamentos activos para verificar.")
        return

    mensajes = []

    for med in medicines:
        nombre = med.get("name")
        stock = med.get("stock", 0)
        min_stock = med.get("minStock", 0)
        fecha_venc = med.get("boxExpirationDate")
        notify = med.get("notifyDaysBefore", 0)

        # 🧮 Convertir fecha
        if isinstance(fecha_venc, str):
            fecha_venc = date.fromisoformat(fecha_venc)

        # 🕒 Calcular si está por vencer
        if notify == 1:
            dias_antes = 7
        else:
            dias_antes = notify * 7  # si algún día usas 2 = dos semanas, etc.

        fecha_alerta = fecha_venc - timedelta(days=dias_antes)
        dias_restantes = (fecha_venc - hoy).days

        # 🔔 1. Por vencer
        if hoy >= fecha_alerta and hoy <= fecha_venc:
            mensajes.append(f"⚠️ El medicamento *{nombre}* está por vencer en {dias_restantes} día(s). Fecha de vencimiento: {fecha_venc}")

        # 🔔 2. Stock bajo
        if stock <= min_stock:
            mensajes.append(f"⚠️ El medicamento *{nombre}* tiene stock bajo ({stock}/{min_stock}).")

    # 2️⃣ Buscar veterinarios (rol 8)
    if not mensajes:
        print("✅ No hay alertas hoy.")
        return

    users_result = await supabase.table("erp_user").select("telegram_chat_id").eq("fk_idUserRole", 8).execute()
    veterinarios = [u["telegram_chat_id"] for u in users_result.data if u.get("telegram_chat_id")]

    if not veterinarios:
        print("⚠️ No hay veterinarios con telegram_chat_id registrado.")
        return

    # 3️⃣ Enviar mensajes
    for chat_id in veterinarios:
        for msg in mensajes:
            url = f"{BASE_URL}/sendMessage"
            payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
            try:
                requests.post(url, data=payload)
            except Exception as e:
                print(f"❌ Error al enviar mensaje a {chat_id}: {e}")

    print(f"✅ Notificaciones enviadas a {len(veterinarios)} veterinario(s).")


def start_scheduler():
    """
    Inicia el verificador automático de medicamentos.
    """
    # Ejecutar todos los días a las 19:35
    scheduler.add_job(
        lambda: asyncio.run(verificar_medicamentos()),
        "cron",
        hour=19,
        minute=40,
    )
    scheduler.start()
    print("🕐 Scheduler de medicamentos iniciado (ejecutará cada día a las 19:40).")
