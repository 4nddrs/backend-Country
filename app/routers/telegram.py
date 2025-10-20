from fastapi import APIRouter, Request
import telebot
import asyncio
from app.supabase_client import get_supabase

router = APIRouter(prefix="/telegram", tags=["Telegram"])

BOT_TOKEN = "8225256599:AAEWeT5H-LP069Gz631-1qBgDOyn6MwS5Zs"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name or ""
    username = message.from_user.username or ""

    # Respuesta al usuario
    bot.reply_to(message, f"¡Hola {first_name or username or 'Veterinario'}! 👋 Tu chat ha sido vinculado con el sistema del Country Club ERP.")

    # Guardar chat_id en Supabase
    asyncio.run(save_telegram_chat(user_id))

async def save_telegram_chat(chat_id: int):
    try:
        supabase = await get_supabase()
        # Buscar veterinarios (rol 8) sin chat_id asignado
        result = await supabase.table("erp_user").select("uid").eq("fk_idUserRole", 8).is_("telegram_chat_id", "null").limit(1).execute()

        if not result.data:
            print("⚠️ No hay veterinarios sin telegram_chat_id pendiente.")
            return

        user_uid = result.data[0]["uid"]

        await supabase.table("erp_user").update({"telegram_chat_id": chat_id}).eq("uid", user_uid).execute()
        print(f"✅ Telegram chat_id {chat_id} vinculado con veterinario UID {user_uid}")
    except Exception as e:
        print(f"❌ Error guardando chat_id: {e}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Repetiste: {message.text}")

@router.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = telebot.types.Update.de_json(data)
        asyncio.get_event_loop().run_in_executor(None, bot.process_new_updates, [update])
        print("✅ Mensaje recibido desde Telegram")
    except Exception as e:
        print("❌ Error procesando actualización de Telegram:", e)
    return {"ok": True}
