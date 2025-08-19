from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.supabase_client import get_supabase  # ✅ usamos supabase en vez de engine/Base
from app.routers import product, employee, employee_position, employee_role

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
