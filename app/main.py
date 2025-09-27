import json
from fastapi import Request
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



@app.middleware("http")
async def _debug_logger(request: Request, call_next):
    method = request.method
    path = request.url.path
    origin = request.headers.get("origin")
    acrm = request.headers.get("access-control-request-method")
    acrh = request.headers.get("access-control-request-headers")

    print(f"[REQ] {method} {path} | Origin={origin} | ACRM={acrm} | ACRH={acrh}")

    # Vista previa del body para POST/PUT/PATCH
    if method in {"POST", "PUT", "PATCH"}:
        raw = await request.body()
        if raw:
            async def _receive():
                return {"type": "http.request", "body": raw, "more_body": False}
            request._receive = _receive
            try:
                print(f"[REQ-BODY] {json.loads(raw.decode('utf-8'))}")
            except Exception:
                print(f"[REQ-BODY] <{len(raw)} bytes>")

    # Responder explícitamente el preflight
    if method == "OPTIONS":
        resp = PlainTextResponse("OK (preflight)", status_code=200)
    else:
        try:
            resp = await call_next(request)
        except Exception as e:
            print(f"[ERROR] {method} {path}: {e}")
            resp = JSONResponse({"detail": str(e)}, status_code=500)

    print(f"[RESP] {method} {path} -> {resp.status_code}")
    return resp


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
