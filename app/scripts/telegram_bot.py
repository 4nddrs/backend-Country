from fastapi import APIRouter, Request
import requests
from app.supabase_client import get_supabase
from app.config import TELEGRAM_BOT_TOKEN

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
router = APIRouter(prefix="/telegram", tags=["Telegram Bot"])


@router.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Webhook principal del bot de Telegram.
    Escucha todos los mensajes enviados al bot y responde según el rol y comando.
    """
    data = await request.json()
    message = data.get("message", {})
    chat_id = str(message.get("chat", {}).get("id"))
    text = (message.get("text") or "").lower().strip()

    if not text:
        return {"ok": True}

    print(f"📩 Mensaje recibido de {chat_id}: {text}")

    # Conexión a Supabase
    supabase = await get_supabase()

    # Buscar usuario por chat_id
    user_q = await supabase.table("erp_user") \
        .select("uid, username, fk_idUserRole, telegram_chat_id, user_role(roleName)") \
        .eq("telegram_chat_id", chat_id) \
        .execute()

    user = user_q.data[0] if user_q.data else None

    # ===============================
    # COMANDO /start → Registro inicial
    # ===============================
    if text == "/start":
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
                await supabase.table("erp_user").update({"telegram_chat_id": chat_id}).eq("uid", user_match["uid"]).execute()
                role_name = user_match["user_role"]["roleName"]
                if role_name == "Admin":
                    reply = (
                        f"✅ Has sido vinculado correctamente como *Administrador* del Country Club.\n\n"
                        f"A partir de ahora recibirás notificaciones automáticas todos los días a las *20:00* 🕗.\n\n"
                        f"Comandos disponibles:\n"
                        "• `/stock_medicamentos` → Ver stock de medicamentos\n"
                        "• `/stock_comida` → Ver stock de alimentos"
                    )
                else:
                    reply = (
                        f"✅ Has sido vinculado correctamente como *Veterinario* del Country Club.\n\n"
                        f"A partir de ahora recibirás alertas automáticas de medicamentos por vencer 🕗.\n\n"
                        f"Comandos disponibles:\n"
                        "• `/stock_medicamentos` → Ver stock de medicamentos"
                    )
                print(f"✅ chat_id {chat_id} vinculado con usuario {user_match['username']} ({role_name})")
            else:
                reply = "⚠️ No se encontró ningún usuario con rol 'Admin' o 'Veterinario' en el sistema."
        else:
            # Ya estaba registrado
            role_name = user["user_role"]["roleName"]
            reply = (
                f"👋 Bienvenido nuevamente, *{user['username']}* ({role_name}).\n\n"
                "Ya estás registrado para recibir notificaciones automáticas a las *20:00* 🕗.\n\n"
                "Comandos disponibles:\n"
                "• `/stock_medicamentos` → Ver stock de medicamentos\n"
                + ("• `/stock_comida` → Ver stock de alimentos" if role_name == "Admin" else "")
            )

        # Enviar respuesta
        requests.post(
            TELEGRAM_URL,
            json={"chat_id": chat_id, "text": reply, "parse_mode": "Markdown"},
        )
        return {"ok": True}

    # ===============================
    # Validar rol permitido
    # ===============================
    if not user or user["user_role"]["roleName"] not in ["Admin", "Veterinario"]:
        requests.post(
            TELEGRAM_URL,
            json={"chat_id": chat_id, "text": "🚫 Solo los administradores o veterinarios pueden usar este bot."},
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
        reply = "❓ Comando no reconocido. Usa /stock_medicamentos o /stock_comida."

    # Enviar respuesta final
    requests.post(
        TELEGRAM_URL,
        json={"chat_id": chat_id, "text": reply, "parse_mode": "Markdown"},
    )

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
        texto = "💊 *Stock de Medicamentos:*\n\n"
        for m in items:
            estado = "🟢" if m["stock"] > m["minStock"] else "🔴"
            texto += f"{estado} {m['name']} — {m['stock']} unidades\n"
        return texto

    elif tabla == "food_stock":
        res = await supabase.table("food_stock").select("foodName, stock, minStock").execute()
        items = res.data or []
        if not items:
            return "⚠️ No hay registros de alimentos."
        texto = "🌾 *Stock de Alimentos:*\n\n"
        for f in items:
            estado = "🟢" if f["stock"] > f["minStock"] else "🔴"
            texto += f"{estado} {f['foodName']} — {f['stock']} kg\n"
        return texto
