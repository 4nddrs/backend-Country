from threading import Thread
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.supabase_client import get_supabase
import requests 
import asyncio
import sys
from app.scheduler import start_scheduler
from app.routers import telegram
from app.routers import (
    employee,
    employee_position,
    food_provider,
    food_stock,
    owner,
    race,
    horse,
    nutritional_plan,
    nutritional_plan_details,
    task_category,
    task,
    alpha_control,
    scheduled_procedure,
    application_procedure,
    medicine,
    attention_horse,
    employee_absence,
    shift_type,
    shift_employed,
    employees_shiftem,
    erp_user,
    user_role,
    expenses,
    income,
    owner_report_month,
    total_control,
    vaccination_plan,
    vaccination_plan_application,
    alpha_report,
    salary_payment,
    tip_payment,
    horse_assignment,
    telegram,
    dashboard,
    camera,
)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title="backend-Country-API")

# ⚡ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://countryclub.doc-ia.cloud",
        "http://localhost:5173",
        "http://localhost:4173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Startup: conexión a Supabase + registro de webhook en Telegram
@app.on_event("startup")
async def on_startup():
    try:
        supabase = await get_supabase()
        await supabase.table("employee_position").select("*").limit(1).execute()
        print("✅ Conexión con Supabase exitosa")
    except Exception as e:
        print("❌ Error de conexión con Supabase:", str(e))

    # 🚀 Configurar el webhook de Telegram automáticamente
    BOT_TOKEN = "8225256599:AAEWeT5H-LP069Gz631-1qBgDOyn6MwS5Zs"
    WEBHOOK_URL = "https://backend-country-nnxe.onrender.com/telegram/webhook"

    try:
        resp = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"
        )
        print("🤖 Webhook configurado:", resp.json())
    except Exception as e:
        print("⚠️ No se pudo registrar el webhook:", str(e))

    # Iniciar el verificador de medicamentos
    start_scheduler()

# ✅ Shutdown: no hace falta cerrar nada en supabase-py
@app.on_event("shutdown")
async def shutdown():
    pass


# Root endpoint
@app.get("/")
async def root():
    return {"message": "API conectada a Supabase DB 🚀"}


# Rutas
app.include_router(employee.router)
app.include_router(employee_position.router)
app.include_router(food_provider.router)
app.include_router(food_stock.router)
app.include_router(owner.router)
app.include_router(race.router)
app.include_router(horse.router)
app.include_router(nutritional_plan.router)
app.include_router(nutritional_plan_details.router)
app.include_router(task_category.router)
app.include_router(task.router)
app.include_router(alpha_control.router)
app.include_router(scheduled_procedure.router)
app.include_router(application_procedure.router)
app.include_router(medicine.router)
app.include_router(attention_horse.router)
app.include_router(employee_absence.router)
app.include_router(shift_type.router)
app.include_router(shift_employed.router)
app.include_router(employees_shiftem.router)
app.include_router(erp_user.router)
app.include_router(user_role.router)
app.include_router(expenses.router)
app.include_router(income.router)
app.include_router(owner_report_month.router)
app.include_router(total_control.router)
app.include_router(vaccination_plan.router)
app.include_router(vaccination_plan_application.router)
app.include_router(alpha_report.router)
app.include_router(salary_payment.router)
app.include_router(tip_payment.router)
app.include_router(horse_assignment.router)
app.include_router(telegram.router)
app.include_router(dashboard.router)
app.include_router(camera.router)

# === 🧪 Endpoint de prueba manual de notificaciones ===
#@app.get("/test-notify")
#async def test_notify():
    #"""
    #Ejecuta manualmente la verificación de medicamentos
    #(sin esperar al scheduler programado).
    #"""
    #from app.scheduler import verificar_medicamentos
    #await verificar_medicamentos()
    #return {"status": "Notificaciones ejecutadas manualmente ✅"}
