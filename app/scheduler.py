from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from app.scripts.telegram_notifier import notificar_alertas_telegram

def start_scheduler():
    scheduler = AsyncIOScheduler(timezone="America/La_Paz")

    # 🔔 Ejecuta todos los días a las 20:00 (8 PM)
    scheduler.add_job(
        notificar_alertas_telegram,
        CronTrigger(hour=20, minute=0),
        id="notificar_alertas_telegram",
        replace_existing=True,
    )

    scheduler.start()
    print(f"🕒 Scheduler iniciado ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) — próxima ejecución a las 20:00")
