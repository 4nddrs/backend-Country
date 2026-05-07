import os
from fastapi import APIRouter, Request, BackgroundTasks
import telebot
from telebot import types
from datetime import date
from app.supabase_client import get_supabase_admin_client

router = APIRouter(prefix="/telegram", tags=["Telegram"])

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


def _parse_fecha(valor):
    if isinstance(valor, str):
        try:
            return date.fromisoformat(valor)
        except Exception:
            return None
    return valor


def _calcular_estado(fecha_venc, notify_days_before, is_active_db):
    """Estado real del medicamento segun la fecha de caducidad."""
    hoy = date.today()
    if fecha_venc is None:
        return ("Activo" if is_active_db else "Inactivo"), None

    dias_restantes = (fecha_venc - hoy).days
    if dias_restantes < 0:
        return "Vencido", dias_restantes

    try:
        notify = int(notify_days_before) if notify_days_before is not None else 1
    except (TypeError, ValueError):
        notify = 1
    dias_alerta = 7 if notify <= 1 else notify * 7

    if dias_restantes <= dias_alerta:
        return "Por vencer", dias_restantes
    return ("Activo" if is_active_db else "Inactivo"), dias_restantes


def _sincronizar_estado_db(supabase, medicines):
    """Marca como inactivos en la BD los medicamentos vencidos para que el frontend tambien lo refleje."""
    hoy = date.today()
    for med in medicines:
        fecha_venc = _parse_fecha(med.get("boxExpirationDate"))
        if not fecha_venc:
            continue
        if fecha_venc < hoy and (med.get("isActive") is None or med.get("isActive") is True):
            try:
                supabase.table("medicine").update(
                    {"isActive": False, "expiryStatus": "Vencido"}
                ).eq("idMedicine", med["idMedicine"]).execute()
                med["isActive"] = False
                med["expiryStatus"] = "Vencido"
            except Exception as e:
                print(f"Error actualizando medicina {med.get('idMedicine')}: {e}")


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

    save_telegram_chat(user_id)


def save_telegram_chat(chat_id: int):
    """Guarda el chat_id del veterinario con rol 8 usando el cliente sincrono."""
    try:
        supabase = get_supabase_admin_client()
        result = (
            supabase.table("erp_user")
            .select("uid")
            .eq("fk_idUserRole", 8)
            .limit(1)
            .execute()
        )
        if result.data:
            uid = result.data[0]["uid"]
            supabase.table("erp_user").update({"telegram_chat_id": chat_id}).eq("uid", uid).execute()
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
    bot.answer_callback_query(call.id)
    try:
        enviar_medicamentos(chat_id, filtro=filtro)
    except Exception as e:
        print(f"❌ Error en callback_handler: {e}")
        bot.send_message(chat_id, f"❌ Error al obtener datos: {e}")


def enviar_medicamentos(chat_id: int, filtro: str):
    """Envía al chat la lista de medicamentos según el filtro (todo sincrono, sin asyncio)."""
    try:
        supabase = get_supabase_admin_client()
        result = supabase.table("medicine").select("*").execute()
        medicines = result.data or []
        print(f"📋 Medicamentos encontrados: {len(medicines)}")
    except Exception as e:
        print(f"❌ Error consultando Supabase: {e}")
        bot.send_message(chat_id, f"❌ Error consultando base de datos: {e}")
        return

    _sincronizar_estado_db(supabase, medicines)

    mensajes = []

    for med in medicines:
        nombre = med.get("name", "Sin nombre")
        stock = med.get("stock", 0)
        min_stock = med.get("minStock", 0)
        fecha_venc = _parse_fecha(med.get("boxExpirationDate"))
        notify_days = med.get("notifyDaysBefore", 1)
        is_active_db = med.get("isActive", True)

        estado, _ = _calcular_estado(fecha_venc, notify_days, is_active_db)

        incluir = False
        if filtro == "medicamentos":
            incluir = True
        elif filtro == "bajo" and stock <= min_stock:
            incluir = True
        elif filtro == "caducado" and estado in ("Vencido", "Por vencer"):
            incluir = True

        if incluir:
            msg = (
                f"Medicamento: {nombre}\n"
                f"Stock: {stock}/{min_stock}\n"
                f"Vence: {fecha_venc if fecha_venc else 'Sin fecha'}\n"
                f"Estado: {estado}"
            )
            mensajes.append(msg)

    if not mensajes:
        texto = "No se encontraron medicamentos para ese criterio."
    else:
        titulos = {
            "medicamentos": "Lista de medicamentos:",
            "bajo": "Medicamentos con stock bajo o agotado:",
            "caducado": "Medicamentos vencidos o por vencer (proximos 7 dias):",
        }
        texto = titulos[filtro] + "\n\n" + "\n\n".join(mensajes)

    bot.send_message(chat_id, texto)


# === Webhook principal ===
@router.post("/webhook")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    """Procesa la actualizacion en background para responder a Telegram al instante."""
    try:
        data = await request.json()
        update = telebot.types.Update.de_json(data)
        background_tasks.add_task(bot.process_new_updates, [update])
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
