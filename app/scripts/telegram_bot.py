import telebot
import threading

BOT_TOKEN = "8225256599:AAEWeT5H-LP069Gz631-1qBgDOyn6MwS5Zs"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! 👋 Bienvenido al bot del Country Club ERP.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Repetiste: {message.text}")

def run_bot():
    print("🤖 Bot de Telegram escuchando mensajes...")
    bot.delete_webhook()  # 👈 necesario para evitar error 409
    bot.infinity_polling()
