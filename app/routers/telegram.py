import os
from fastapi import APIRouter, Request
import telebot
from telebot import types
import asyncio
from datetime import date
from app.supabase_client import get_supabase

router = APIRouter(prefix="/telegram", tags=["Telegram"])

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def run_async(coro):
    """Ejecuta una coroutine desde un hilo sincrónico (handlers de telebot)."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# === /start ===
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name or ""

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🧾 Ver medicamentos", callback_data="medicamentos")
    btn2 = types.InlineKeyboardButton("⚠️ Stock bajo / agotado", callback_data="bajo")
    btn3 = types.InlineKeyboardButton("⏰ Por vencer / vencidos", callback_data="caducado")
    markup.add(btn1)
    markup.add(btn2, btn3)

    bot.send_message(
        message.chat.id,
        f"👋 ¡Hola {first_name or 'Veterinario'}!\n"
        "Tu chat ha sido vinculado con el sistema del *Country Club ERP*.\n\n"
        "Selecciona una opción del menú 👇",
        reply_markup=markup,
        parse_mode="Markdown",
    )

    run_async(save_telegram_chat(user_id))


async def save_telegram_chat(chat_id: int):
    """Guarda el chat_id del veterinario con rol 8 (actualiza aunque ya tenga uno)."""
    try:
        supabase = await get_supabase()
        result = await (
            supabase.table("erp_user")
            .select("uid")
            .eq("fk_idUserRole", 8)
            .limit(1)
            .execute()
        )
        if result.data:
            uid = result.data[0]["uid"]
            await supabase.table("erp_user").update({"telegram_chat_id": chat_id}).eq("uid", uid).execute()
            print(f"✅ Veterinario vinculado: {uid} -> chat {chat_id}")
        else:
            print(f"⚠️ No se encontró usuario con rol 8. chat_id recibido: {chat_id}")
    except Exception as e:
        print("❌ Error guardando chat_id:", e)


# === CALLBACKS DE BOTONES ===
@bot.callback_query_handler(func=lambda call: call.data in ["medicamentos", "bajo", "caducado"])
def callback_handler(call):
    filtro = call.data
    chat_id = call.message.chat.id
    run_async(enviar_medicamentos(chat_id, filtro=filtro))


async def enviar_medicamentos(chat_id: int, filtro: str):
    """Envía al chat la lista de medicamentos según el filtro."""
    supabase = await get_supabase()
    result = await supabase.table("medicine").select("*").execute()
    medicines = result.data or []

    hoy = date.today()
    mensajes = []

    for med in medicines:
        nombre = med.get("name", "Sin nombre")
        stock = med.get("stock", 0)
        min_stock = med.get("minStock", 0)
        fecha_venc = med.get("boxExpirationDate")
        is_active = med.get("isActive", True)

        if isinstance(fecha_venc, str):
            try:
                fecha_venc = date.fromisoformat(fecha_venc)
            except Exception:
                fecha_venc = None

        dias_restantes = (fecha_venc - hoy).days if fecha_venc else None
        estado = "Activo ✅" if is_active else "Inactivo ❌"

        incluir = False
        if filtro == "medicamentos":
            incluir = True
        elif filtro == "bajo" and stock <= min_stock:
            incluir = True
        elif filtro == "caducado" and fecha_venc:
            if dias_restantes <= 7:
                incluir = True

        if incluir:
            msg = (
                f"💊 *{nombre}*\n"
                f"📦 Stock: {stock}/{min_stock}\n"
                f"📅 Vence: {fecha_venc if fecha_venc else 'Sin fecha'}\n"
                f"🔖 Estado: {estado}"
            )
            mensajes.append(msg)

    if not mensajes:
        texto = "✅ No se encontraron medicamentos para ese criterio."
    else:
        titulo = {
            "medicamentos": "🧾 *Lista de medicamentos:*",
            "bajo": "⚠️ *Medicamentos con stock bajo o agotado:*",
            "caducado": "⏰ *Medicamentos vencidos o por vencer:*",
        }[filtro]
        texto = titulo + "\n\n" + "\n\n".join(mensajes)

    bot.send_message(chat_id, texto, parse_mode="Markdown")


# === Webhook principal ===
@router.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = telebot.types.Update.de_json(data)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, bot.process_new_updates, [update])
        print("✅ Mensaje recibido desde Telegram")
    except Exception as e:
        print("❌ Error procesando actualización de Telegram:", e)
    return {"ok": True}


# === Registrar webhook con Telegram ===
@router.get("/setup-webhook")
async def setup_webhook(webhook_url: str):
    """
    Registra la URL del webhook con Telegram.
    Llama a: GET /telegram/setup-webhook?webhook_url=https://tu-dominio.com/telegram/webhook
    """
    response = bot.set_webhook(url=webhook_url)
    if response:
        return {"ok": True, "message": f"Webhook registrado en: {webhook_url}"}
    return {"ok": False, "message": "Error al registrar el webhook"}
