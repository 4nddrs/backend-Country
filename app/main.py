from fastapi import FastAPI
from app.database import engine, Base
from app.routers import product

app = FastAPI(title="backend-Country-API")


@app.on_event("startup")
async def on_startup():
    # Crear tablas si no existen, sin abrir sesiones adicionales
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    # No necesitamos desconectar explícitamente con asyncpg + PgBouncer
    pass


@app.get("/")
async def root():
    return {"message": "API connected to Supabase DB!"}


# Rutas
app.include_router(product.router)
