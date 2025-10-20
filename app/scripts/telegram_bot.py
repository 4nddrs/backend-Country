from fastapi import APIRouter, Request
from html import escape
import httpx

from app.supabase_client import get_supabase
from app.scripts.telegram_client import send_message

router = APIRouter(prefix="/telegram", tags=["Telegram Bot"])


async def _responder(chat_id: str, texto: str) -> None:
    try:
        await send_message(chat_id, texto)
    except httpx.HTTPStatusError as exc:
        print(
            f"❌ Error HTTP enviando respuesta a {chat_id}: "
            f"{exc.response.status_code} {exc.response.text}"
        )
    except (httpx.RequestError, RuntimeError) as exc:
        print(f"❌ Error al enviar respuesta a {chat_id}: {exc}")


@router.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Webhook principal del bot de Telegram.
    Escucha todos los mensajes enviados al bot y responde según el rol y comando.
    """
    data = await request.json()

    message = data.get("message")
    if not message:
        print(f"⚠️ Payload recibido sin 'message': {data}")
        return {"ok": True}

    chat = message.get("chat") or {}
    chat_id_raw = chat.get("id")
    if chat_id_raw is None:
        print(f"⚠️ Mensaje sin chat_id: {message}")
        return {"ok": True}

    chat_id_int = int(chat_id_raw)
    chat_id_str = str(chat_id_int)

    text_raw = message.get("text")
    text = (text_raw or "").strip()
    text_lower = text.lower()

    if not text:
        return {"ok": True}

    print(f"📩 Mensaje recibido de {chat_id_str}: {text}")

    # Conexión a Supabase
    supabase = await get_supabase()

    # Buscar usuario por chat_id
    user_q = (
        await supabase.table("erp_user")
        .select("uid, username, fk_idUserRole, telegram_chat_id, user_role(roleName)")
        .eq("telegram_chat_id", chat_id_int)
        .execute()
    )

    user = user_q.data[0] if user_q.data else None
    if not user:
        # Intento secundario comparando como texto (por compatibilidad con columnas tipo texto)
        user_q = (
            await supabase.table("erp_user")
            .select("uid, username, fk_idUserRole, telegram_chat_id, user_role(roleName)")
            .eq("telegram_chat_id", chat_id_str)
            .execute()
        )
        user = user_q.data[0] if user_q.data else None


    # ===============================
    # COMANDO /start → Registro inicial
    # ===============================
    if text_lower == "/start":
        if not user:
            # Buscar un usuario con rol Admin o Veterinario
            roles_permitidos = [6, 8]  # 6 = Admin, 8 = Veterinario
            rol_q = await supabase.table("erp_user") \
                .select("uid, username, fk_idUserRole, user_role(roleName)") \
                .in_("fk_idUserRole", roles_permitidos) \
                .limit(1) \
                .execute()

            user_match = rol_q.data[0] if rol_q.data else None
            if user_match:
                # Vincular chat_id con usuario permitido
                try:
                    await supabase.table("erp_user").update(
                        {"telegram_chat_id": chat_id_int}
                    ).eq("uid", user_match["uid"]).execute()
                except Exception as exc:
                    print(f"⚠️ Error guardando telegram_chat_id como número: {exc}. Reintentando como texto.")
                    await supabase.table("erp_user").update(
                        {"telegram_chat_id": chat_id_str}
                    ).eq("uid", user_match["uid"]).execute()
                role_name = user_match["user_role"]["roleName"]
                if role_name == "Admin":
                    reply = (
                        "✅ Has sido vinculado correctamente como <b>Administrador</b> del Country Club.\n\n"
                        "A partir de ahora recibirás notificaciones automáticas todos los días a las <b>20:00</b> 🕗.\n\n"
                        "Comandos disponibles:\n"
                        "• <code>/stock_medicamentos</code> → Ver stock de medicamentos\n"
                        "• <code>/stock_comida</code> → Ver stock de alimentos"
                    )
                else:
                    reply = (
                        "✅ Has sido vinculado correctamente como <b>Veterinario</b> del Country Club.\n\n"
                        "A partir de ahora recibirás alertas automáticas de medicamentos por vencer 🕗.\n\n"
                        "Comandos disponibles:\n"
                        "• <code>/stock_medicamentos</code> → Ver stock de medicamentos"
                    )
                print(f"✅ chat_id {chat_id} vinculado con usuario {user_match['username']} ({role_name})")
            else:
                reply = "⚠️ No se encontró ningún usuario con rol 'Admin' o 'Veterinario' en el sistema."
        else:
            # Ya estaba registrado
            role_name = user["user_role"]["roleName"]
            reply = (
                f"👋 Bienvenido nuevamente, <b>{escape(user['username'])}</b> ({escape(role_name)}).\n\n"
                "Ya estás registrado para recibir notificaciones automáticas a las <b>20:00</b> 🕗.\n\n"
                "Comandos disponibles:\n"
                "• <code>/stock_medicamentos</code> → Ver stock de medicamentos\n"
                + ("• <code>/stock_comida</code> → Ver stock de alimentos" if role_name == "Admin" else "")
            )

        # Enviar respuesta
        await _responder(chat_id_str, reply)
        return {"ok": True}

    # ===============================
    # Validar rol permitido
    # ===============================
    if not user or user["user_role"]["roleName"] not in ["Admin", "Veterinario"]:
        await _responder(
            chat_id_str,
            "🚫 Solo los administradores o veterinarios pueden usar este bot.",
        )
        return {"ok": True}

    role_name = user["user_role"]["roleName"]

    # ===============================
    # Comandos secundarios
    # ===============================
    if text == "/stock_medicamentos":
        reply = await obtener_stock("medicine")
    elif text == "/stock_comida":
        if role_name == "Admin":
            reply = await obtener_stock("food_stock")
        else:
            reply = "🚫 Solo los administradores pueden consultar el stock de alimentos."
    else:
        reply = "❓ Comando no reconocido. Usa <code>/stock_medicamentos</code> o <code>/stock_comida</code>."

    # Enviar respuesta final
    await _responder(chat_id_str, reply)

    return {"ok": True}


# ============================================================
# Función auxiliar: obtener stock de medicamentos y alimentos
# ============================================================
async def obtener_stock(tabla: str):
    supabase = await get_supabase()

    if tabla == "medicine":
        res = await supabase.table("medicine").select("name, stock, minStock").execute()
        items = res.data or []
        if not items:
            return "⚠️ No hay registros de medicamentos."
        texto = "💊 <b>Stock de Medicamentos:</b>\n\n"
        for m in items:
            estado = "🟢" if m["stock"] > m["minStock"] else "🔴"
            texto += f"{estado} {escape(m['name'])} — {m['stock']} unidades\n"
        return texto

    elif tabla == "food_stock":
        res = await supabase.table("food_stock").select("foodName, stock, minStock").execute()
        items = res.data or []
        if not items:
            return "⚠️ No hay registros de alimentos."
        texto = "🌾 <b>Stock de Alimentos:</b>\n\n"
        for f in items:
            estado = "🟢" if f["stock"] > f["minStock"] else "🔴"
            texto += f"{estado} {escape(f['foodName'])} — {f['stock']} kg\n"
        return texto
