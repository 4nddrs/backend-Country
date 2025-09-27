# main.py (fragmento)
import json
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse

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
    expenses,
    income,
    owner_report_month,
    total_control,
    vaccination_plan,
    vaccination_plan_application,
    alpha_report,
    salary_payment,
)

app = FastAPI(title="backend-Country-API")

# ---------- CORS CORRECTO ----------
# Opción A (recomendada): lista explícita y credenciales permitidas
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # agrega tu dominio real si tienes front en producción
    # "https://tu-frontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,      # ok porque NO usamos "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Si insistes en permitir todo en dev:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=False,    # IMPORTANTE si usas "*"
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# ---------- LOGGING + CORS SIEMPRE (incluye errores y preflight) ----------
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("app")

@app.middleware("http")
async def debug_and_force_cors(request: Request, call_next):
    method = request.method
    path = request.url.path
    origin = request.headers.get("origin")
    acrm = request.headers.get("access-control-request-method")
    acrh = request.headers.get("access-control-request-headers")

    print(f"[REQ] {method} {path} | Origin={origin} | ACRM={acrm} | ACRH={acrh}")

    # Vista previa de body en POST/PUT/PATCH (sin romper el stream)
    body_preview = None
    try:
        if method in {"POST", "PUT", "PATCH"}:
            raw = await request.body()
            if raw:
                async def receive_gen():
                    return {"type": "http.request", "body": raw, "more_body": False}
                request._receive = receive_gen
                try:
                    body_preview = json.loads(raw.decode("utf-8"))
                except Exception:
                    body_preview = f"<{len(raw)} bytes>"
        print(f"[REQ-BODY] {body_preview}")
    except Exception as e:
        print(f"[REQ-BODY] no legible: {e}")

    # Preflight explícito
    if method == "OPTIONS":
        resp = PlainTextResponse("OK (preflight)", status_code=200)
    else:
        try:
            resp = await call_next(request)
        except Exception as e:
            # Log del error real (stacktrace) y respuesta 500 JSON
            log.exception(f"[ERROR] {method} {path}: {e}")
            resp = JSONResponse({"detail": str(e)}, status_code=500)

    # Asegurar CORS headers SIEMPRE
    if origin and (origin in ALLOWED_ORIGINS or "*" in ALLOWED_ORIGINS):
        resp.headers["Access-Control-Allow-Origin"] = origin if origin in ALLOWED_ORIGINS else "*"
        # Si usas "*" arriba, NO pongas credentials
        if origin in ALLOWED_ORIGINS:
            resp.headers["Access-Control-Allow-Credentials"] = "true"
        resp.headers["Vary"] = "Origin"
        resp.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = acrh or "*"

    print(f"[RESP] {method} {path} -> {resp.status_code}")
    return resp

# Endpoints de diagnóstico (opcionales)
@app.get("/_debug/cors")
def debug_cors():
    return {"ok": True}

@app.options("/_debug/cors")
def debug_cors_options():
    return PlainTextResponse("OK (debug options)")

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
app.include_router(expenses.router)
app.include_router(income.router)
app.include_router(owner_report_month.router)
app.include_router(total_control.router)
app.include_router(vaccination_plan.router)
app.include_router(vaccination_plan_application.router)
app.include_router(alpha_report.router)
app.include_router(salary_payment.router)