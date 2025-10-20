# app/scripts/telegram_notifier.py
from datetime import date
from app.supabase_client import get_supabase
from app.config import TELEGRAM_BOT_TOKEN
import requests

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


async def notificar_alertas_telegram():
    """Notifica por Telegram cuando hay medicamentos por vencer o stock bajo."""
    print("🚀 Iniciando verificación automática de vencimientos y stock mínimo...")

    supabase = await get_supabase()
    hoy = date.today()

    # 1️⃣ Obtener lista de usuarios (Admins y Veterinarios)
    query_users = await supabase.table("erp_user") \
        .select("uid, username, telegram_chat_id, user_role(roleName)") \
        .in_("fk_idUserRole", [6, 8]) \
        .execute()

    users = [u for u in (query_users.data or []) if u.get("telegram_chat_id")]
    print(f"👥 Usuarios válidos encontrados: {len(users)}")

    if not users:
        print("⚠️ No hay usuarios con telegram_chat_id registrados.")
        return

    # 2️⃣ Verificar medicamentos por vencer
    meds_result = await supabase.table("medicine").select("*").execute()
    medicamentos = meds_result.data or []

    medicamentos_por_vencer = []
    stock_bajo = []

    for med in medicamentos:
        nombre = med.get("name")
        stock = med.get("stock", 0)
        min_stock = med.get("minStock", 0)
        fecha_venc = med.get("boxExpirationDate")
        semanas_aviso = med.get("notifyDaysBefore")

        if not fecha_venc or not semanas_aviso:
            continue

        dias_aviso = int(semanas_aviso) * 7
        dias_restantes = (date.fromisoformat(fecha_venc) - hoy).days

        if 0 < dias_restantes <= dias_aviso:
            medicamentos_por_vencer.append((nombre, fecha_venc, dias_restantes))

        if stock <= min_stock:
            stock_bajo.append((nombre, stock, min_stock))

    # 3️⃣ Enviar notificaciones
    for user in users:
        chat_id = user["telegram_chat_id"]
        role = user["user_role"]["roleName"]

        mensajes = []

        # Veterinario y Admin reciben alertas de vencimiento
        if medicamentos_por_vencer:
            msg = "⚠️ *Medicamentos próximos a vencer:*\n"
            for m in medicamentos_por_vencer:
                msg += f"• {m[0]} — vence el {m[1]} (faltan {m[2]} días)\n"
            mensajes.append(msg)
        else:
            mensajes.append("✅ No hay medicamentos próximos a vencer.")

        # Solo Admin recibe alertas de stock bajo
        if role == "Admin":
            if stock_bajo:
                msg = "\n📦 *Productos con stock bajo:*\n"
                for s in stock_bajo:
                    msg += f"• {s[0]} — {s[1]} / {s[2]} unidades mínimas\n"
                mensajes.append(msg)
            else:
                mensajes.append("\n🟢 Todo el stock se encuentra dentro de niveles normales.")

        # Unir mensajes
        texto_final = "\n".join(mensajes)

        try:
            requests.post(
                TELEGRAM_URL,
                json={"chat_id": chat_id, "text": texto_final, "parse_mode": "Markdown"},
            )
            print(f"📨 Notificación enviada a {user['username']} ({role})")
        except Exception as e:
            print(f"❌ Error al enviar mensaje a {user['username']} ({role}): {e}")

    print("✅ Verificación y envío de alertas completados.")
