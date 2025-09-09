from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.supabase_client import get_supabase  # ✅ usamos supabase en vez de engine/Base
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
)

app = FastAPI(title="backend-Country-API")

# ⚡ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier dominio (para pruebas)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Startup: probar conexión a Supabase
@app.on_event("startup")
async def on_startup():
    try:
        supabase = await get_supabase()
        response = (
            await supabase.table("employee_position").select("*").limit(1).execute()
        )
        print("✅ Conexión con Supabase exitosa")
    except Exception as e:
        print("❌ Error de conexión con Supabase:", str(e))


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
