from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from app.supabase_client import get_supabase
import asyncio
import requests

BOT_TOKEN = "8225256599:AAEWeT5H-LP069Gz631-1qBgDOyn6MwS5Zs"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

scheduler = BackgroundScheduler()

async def verificar_medicamentos():
    """
    Revisa medicamentos por vencer o con stock bajo y notifica al veterinario.
    """
    print("🔍 Iniciando verificación de medicamentos...")
    supabase = await get_supabase()
    hoy = date.today()

    # 1️⃣ Obtener todos los medicamentos activos (aunque estén agotados)
    result = await supabase.table("medicine").select("*").execute()
    medicines = result.data or []

    if not medicines:
        print("📦 No hay medicamentos registrados.")
        return

    mensajes = []

    for med in medicines:
        nombre = med.get("name", "Desconocido")
        stock = med.get("stock", 0)
        min_stock = med.get("minStock", 0)
        fecha_venc = med.get("boxExpirationDate")
        notify = med.get("notifyDaysBefore", 1)
        is_active = med.get("isActive", True)

        # Convertir fecha si es string
        if isinstance(fecha_venc, str):
            try:
                fecha_venc = date.fromisoformat(fecha_venc)
            except Exception:
                fecha_venc = None

        # 🧮 Calcular alertas
        # 1. Stock bajo o agotado
        if stock <= min_stock:
            estado_stock = "agotado" if stock == 0 else "bajo"
            mensajes.append(
                f"⚠️ *Alerta de Stock*:\nEl medicamento *{nombre}* tiene stock {estado_stock} ({stock}/{min_stock})."
            )

        # 2. Próximo a vencer
        if fecha_venc:
            dias_antes = 7 if notify == 1 else notify * 7
            fecha_alerta = fecha_venc - timedelta(days=dias_antes)
            dias_restantes = (fecha_venc - hoy).days
            if hoy >= fecha_alerta and hoy <= fecha_venc:
                mensajes.append(
                    f"⚠️ *Medicamento por vencer*:\n*{nombre}* vence el {fecha_venc} (en {dias_restantes} día(s))."
                )

    # 2️⃣ Si no hay mensajes, salir
    if not mensajes:
        print("✅ No hay alertas hoy.")
        return

    # 3️⃣ Buscar veterinarios (rol 8 con telegram_chat_id)
    users_result = await supabase.table("erp_user").select("telegram_chat_id").eq("fk_idUserRole", 8).execute()
    veterinarios = [u["telegram_chat_id"] for u in users_result.data if u.get("telegram_chat_id")]

    if not veterinarios:
        print("⚠️ No hay veterinarios con telegram_chat_id registrado.")
        return

    # 4️⃣ Enviar mensajes
    for chat_id in veterinarios:
        for msg in mensajes:
            url = f"{BASE_URL}/sendMessage"
            payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
            try:
                response = requests.post(url, data=payload)
                if response.status_code != 200:
                    print(f"❌ Error enviando a {chat_id}: {response.text}")
            except Exception as e:
                print(f"❌ Excepción al enviar mensaje a {chat_id}: {e}")

    print(f"✅ Notificaciones enviadas ({len(mensajes)} alertas a {len(veterinarios)} veterinario(s)).")

def start_scheduler():
    """
    Inicia el verificador automático de medicamentos.
    """
    scheduler.add_job(
        lambda: asyncio.run(verificar_medicamentos()),
        "cron",
        hour=21,  # UTC = 19 Bolivia
        minute=1,
    )
    scheduler.start()
    print("🕐 Scheduler de medicamentos iniciado (ejecutará cada día a las 19:35 Bolivia / 23:35 UTC).")
