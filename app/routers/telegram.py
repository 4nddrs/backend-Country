from fastapi import APIRouter, Request
import telebot

router = APIRouter(prefix="/telegram", tags=["Telegram"])

BOT_TOKEN = "8225256599:AAEWeT5H-LP069Gz631-1qBgDOyn6MwS5Zs"
bot = telebot.TeleBot(BOT_TOKEN)

# === Comandos ===
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! 👋 Bienvenido al bot del Country Club ERP.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Repetiste: {message.text}")

# === Webhook ===
@router.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = telebot.types.Update.de_json(data)
    bot.process_new_updates([update])
    return {"ok": True}
