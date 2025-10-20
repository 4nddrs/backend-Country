import os

from dotenv import load_dotenv

# Cargar automáticamente variables desde .env (si existen)
load_dotenv()

# Valores por defecto (fallback) cuando no hay variables de entorno definidas
DEFAULT_SUPABASE_URL = "https://dqhtzvkbgjhnjnmcixcp.supabase.co"
DEFAULT_SUPABASE_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRxaHR6dmti"
    "Z2pobmpubWNpeGNwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTAxNjAzOCwiZXhwIjoy"
    "MDcwNTkyMDM4fQ.VAGtVi21XIXZWRsX0lzfUIZXWZPwWOvkVgaPtPET6R0"
)
DEFAULT_TELEGRAM_TOKEN = "8225256599:AAEWeT5H-LP069Gz631-1qBgDOyn6MwS5Zs"

# ✅ Supabase (usa variable de entorno o el valor por defecto)
SUPABASE_URL = os.getenv("SUPABASE_URL", DEFAULT_SUPABASE_URL)
SUPABASE_KEY = os.getenv("SUPABASE_KEY", DEFAULT_SUPABASE_KEY)

# ✅ Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", DEFAULT_TELEGRAM_TOKEN)

# Mensaje informativo
if all(
    [
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY"),
        os.getenv("TELEGRAM_BOT_TOKEN"),
    ]
):
    print("✅ [config.py] Variables de entorno cargadas correctamente.")
else:
    print("ℹ️ [config.py] Usando valores por defecto definidos en config.py.")
