from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.supabase_client import get_supabase  # ✅ usamos supabase en vez de engine/Base
from app.routers import (
    product,
    employee,
    employee_position,
    employee_role,
    food_provider,
    food_stock,
    vaccine,
    owner,
    race,
    horse,
    nutritional_plan, 
    nutritional_plan_horse,
    nutritional_plan_details,
    task_category,
    task,
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
        response = await supabase.table("employee_role").select("*").limit(1).execute()
        print("✅ Conexión con Supabase exitosa:", response.data)
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
app.include_router(product.router)
app.include_router(employee.router)
app.include_router(employee_position.router)
app.include_router(employee_role.router)
app.include_router(food_provider.router)
app.include_router(food_stock.router)
app.include_router(vaccine.router)
app.include_router(owner.router)
app.include_router(race.router)
app.include_router(horse.router)
app.include_router(nutritional_plan.router)
app.include_router(nutritional_plan_horse.router)
app.include_router(nutritional_plan_details.router)
app.include_router(task_category.router)
app.include_router(task.router)
