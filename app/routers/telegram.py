import os
import threading
from fastapi import APIRouter, Request, BackgroundTasks
import telebot
from telebot import types
from datetime import date
from app.supabase_client import get_supabase_admin_client

router = APIRouter(prefix="/telegram", tags=["Telegram"])

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

SEPARADOR = "━━━━━━━━━━━━━━━━━━"
ICONO_MED = "❖"
TG_LIMIT = 3500  # margen seguro bajo el limite de 4096 de Telegram


def _parse_fecha(valor):
    if isinstance(valor, str):
        try:
            return date.fromisoformat(valor)
        except Exception:
            return None
    return valor


def _esc(texto) -> str:
    """Escapa caracteres reservados de HTML para Telegram."""
    if texto is None:
        return ""
    return (
        str(texto)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


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


def _texto_dias(dias_restantes):
    if dias_restantes is None:
        return ""
    if dias_restantes < 0:
        return f" (hace {-dias_restantes} día{'s' if -dias_restantes != 1 else ''})"
    if dias_restantes == 0:
        return " (vence hoy)"
    return f" (en {dias_restantes} día{'s' if dias_restantes != 1 else ''})"


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


def _build_menu_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🧾 Ver medicamentos", callback_data="medicamentos"))
    markup.add(
        types.InlineKeyboardButton("⚠️ Stock bajo", callback_data="bajo"),
        types.InlineKeyboardButton("⏰ Por vencer", callback_data="caducado"),
    )
    return markup


def _enviar_lista_con_menu(chat_id: int, texto: str):
    """Envia el texto respetando el limite de Telegram. Adjunta el menu al ultimo trozo."""
    menu = _build_menu_markup()

    if len(texto) <= TG_LIMIT:
        bot.send_message(
            chat_id, texto, parse_mode="HTML", disable_web_page_preview=True, reply_markup=menu
        )
        return

    bloques = texto.split(f"\n{SEPARADOR}\n")
    chunks = []
    buffer = ""
    for i, bloque in enumerate(bloques):
        pieza = bloque if i == 0 else f"\n{SEPARADOR}\n{bloque}"
        if len(buffer) + len(pieza) > TG_LIMIT and buffer:
            chunks.append(buffer)
            buffer = bloque
        else:
            buffer += pieza
    if buffer:
        chunks.append(buffer)

    ultimo = len(chunks) - 1
    for i, chunk in enumerate(chunks):
        bot.send_message(
            chat_id,
            chunk,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=menu if i == ultimo else None,
        )


def _format_medicamento(med: dict) -> tuple[str, str]:
    """Devuelve (estado, texto_html) para un medicamento. Sin iconos a color en los campos."""
    nombre = med.get("name", "Sin nombre")
    stock = med.get("stock", 0) or 0
    min_stock = med.get("minStock", 0) or 0
    fecha_venc = _parse_fecha(med.get("boxExpirationDate"))
    notify_days = med.get("notifyDaysBefore", 1)
    is_active_db = med.get("isActive", True)
    tipo = med.get("medicationType")

    estado, dias = _calcular_estado(fecha_venc, notify_days, is_active_db)
    fecha_txt = fecha_venc.strftime("%d/%m/%Y") if fecha_venc else "Sin fecha"
    dias_txt = _texto_dias(dias) if fecha_venc else ""
    tipo_txt = f"\n   <i>{_esc(tipo)}</i>" if tipo else ""

    texto = (
        f"{ICONO_MED} <b>{_esc(nombre)}</b>{tipo_txt}\n"
        f"   Stock: <b>{stock}</b> / mín {min_stock}\n"
        f"   Vence: <b>{fecha_txt}</b>{dias_txt}\n"
        f"   Estado: <b>{estado}</b>"
    )
    return estado, texto


# === /start ===
@bot.message_handler(commands=["start", "help", "menu"])
def send_welcome(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name or ""

    bot.send_message(
        message.chat.id,
        (
            f"👋 ¡Hola <b>{_esc(first_name) or 'Veterinario'}</b>!\n"
            "Tu chat fue vinculado al sistema del <b>Country Club ERP</b>.\n\n"
            "Selecciona una opción del menú 👇"
        ),
        reply_markup=_build_menu_markup(),
        parse_mode="HTML",
    )

    # Diferimos el guardado en BD a un hilo: no afecta la latencia percibida del /start
    threading.Thread(target=save_telegram_chat, args=(user_id,), daemon=True).start()


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
        bot.send_message(
            chat_id,
            f"❌ Error al obtener datos: {_esc(e)}",
            parse_mode="HTML",
            reply_markup=_build_menu_markup(),
        )


def enviar_medicamentos(chat_id: int, filtro: str):
    """Envía al chat la lista de medicamentos según el filtro (todo sincrono, sin asyncio)."""
    try:
        supabase = get_supabase_admin_client()
        result = supabase.table("medicine").select("*").execute()
        medicines = result.data or []
        print(f"📋 Medicamentos encontrados: {len(medicines)}")
    except Exception as e:
        print(f"❌ Error consultando Supabase: {e}")
        bot.send_message(
            chat_id,
            f"❌ Error consultando base de datos: {_esc(e)}",
            parse_mode="HTML",
            reply_markup=_build_menu_markup(),
        )
        return

    _sincronizar_estado_db(supabase, medicines)

    bloques = []

    for med in medicines:
        stock = med.get("stock", 0) or 0
        min_stock = med.get("minStock", 0) or 0
        fecha_venc = _parse_fecha(med.get("boxExpirationDate"))
        notify_days = med.get("notifyDaysBefore", 1)
        is_active_db = med.get("isActive", True)
        estado, _dias = _calcular_estado(fecha_venc, notify_days, is_active_db)

        incluir = False
        if filtro == "medicamentos":
            incluir = True
        elif filtro == "bajo" and stock <= min_stock:
            incluir = True
        elif filtro == "caducado" and estado in ("Vencido", "Por vencer"):
            incluir = True

        if incluir:
            _, texto = _format_medicamento(med)
            bloques.append(texto)

    titulos = {
        "medicamentos": ("🧾", "Lista de medicamentos"),
        "bajo": ("⚠️", "Stock bajo o agotado"),
        "caducado": ("⏰", "Vencidos / próximos a vencer"),
    }
    icono_t, titulo = titulos.get(filtro, ("📋", "Resultados"))

    if not bloques:
        bot.send_message(
            chat_id,
            f"{icono_t} <b>{titulo}</b>\n\nℹ️ No se encontraron medicamentos para ese criterio.",
            parse_mode="HTML",
            reply_markup=_build_menu_markup(),
        )
        return

    encabezado = (
        f"{icono_t} <b>{titulo}</b>\n"
        f"<i>Total: {len(bloques)} medicamento(s)</i>\n"
        f"{SEPARADOR}\n"
    )
    cuerpo = f"\n{SEPARADOR}\n".join(bloques)
    _enviar_lista_con_menu(chat_id, encabezado + cuerpo)


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
