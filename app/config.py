from dotenv import load_dotenv
import os

# Cargar automáticamente variables desde .env
load_dotenv()

# 🔹 Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 🔹 Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Verificación opcional (solo para depuración local)
if not all([SUPABASE_URL, SUPABASE_KEY, TELEGRAM_BOT_TOKEN]):
    print("⚠️ [config.py] Faltan variables de entorno (.env no cargado o incompleto).")
else:
    print("✅ [config.py] Variables de entorno cargadas correctamente.")
