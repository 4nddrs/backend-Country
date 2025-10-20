# app/scripts/telegram_notifier.py
from datetime import date
from html import escape
from typing import List, Tuple

import httpx

from app.supabase_client import get_supabase
from app.scripts.telegram_client import send_message


async def notificar_alertas_telegram():
    """Notifica por Telegram cuando hay medicamentos por vencer o stock bajo."""
    print("🚀 Iniciando verificación automática de vencimientos y stock mínimo...")

    supabase = await get_supabase()
    hoy = date.today()

    # 1️⃣ Obtener lista de usuarios (Admins y Veterinarios)
    query_users = await (
        supabase.table("erp_user")
        .select("uid, username, telegram_chat_id, user_role(roleName)")
        .in_("fk_idUserRole", [6, 8])
        .execute()
    )

    users = [u for u in (query_users.data or []) if u.get("telegram_chat_id")]
    print(f"👥 Usuarios válidos encontrados: {len(users)}")

    if not users:
        print("⚠️ No hay usuarios con telegram_chat_id registrados.")
        return

    # 2️⃣ Verificar medicamentos por vencer
    meds_result = await supabase.table("medicine").select("*").execute()
    medicamentos = meds_result.data or []

    medicamentos_por_vencer: List[Tuple[str, str, int]] = []

    for med in medicamentos:
        nombre = med.get("name")
        fecha_venc = med.get("boxExpirationDate")
        semanas_aviso = med.get("notifyDaysBefore")

        if not nombre or not fecha_venc or not semanas_aviso:
            continue

        try:
            dias_aviso = int(semanas_aviso) * 7
        except (TypeError, ValueError):
            print(f"⚠️ notifyDaysBefore inválido para {nombre}: {semanas_aviso}")
            continue

        try:
            dias_restantes = (date.fromisoformat(str(fecha_venc)) - hoy).days
        except ValueError:
            print(f"⚠️ Formato de fecha inválido para {nombre}: {fecha_venc}")
            continue

        if 0 < dias_restantes <= dias_aviso:
            medicamentos_por_vencer.append((nombre, str(fecha_venc), dias_restantes))

    if not medicamentos_por_vencer:
        print("ℹ️ No hay medicamentos dentro de la ventana de aviso. No se envían notificaciones.")
        return

    # 3️⃣ Enviar notificaciones
    for user in users:
        chat_id = user["telegram_chat_id"]
        role = user["user_role"]["roleName"]

        secciones = []

        lineas = ["<b>Medicamentos próximos a vencer:</b>"]
        for nombre, fecha, dias in medicamentos_por_vencer:
            lineas.append(
                f"• {escape(nombre)} — vence el {escape(fecha)} (faltan {dias} días)"
            )
        secciones.append("\n".join(lineas))

        texto_final = "\n\n".join(secciones)

        try:
            await send_message(chat_id, texto_final)
            print(f"📨 Notificación enviada a {user['username']} ({role})")
        except httpx.HTTPStatusError as exc:
            print(
                f"❌ Error HTTP enviando mensaje a {user['username']} ({role}): "
                f"{exc.response.status_code} {exc.response.text}"
            )
        except (httpx.RequestError, RuntimeError) as exc:
            print(f"❌ Error al enviar mensaje a {user['username']} ({role}): {exc}")

    print("✅ Verificación y envío de alertas completados.")
