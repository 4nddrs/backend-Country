from fastapi import FastAPI
from app.database import database, engine, Base
from app.routers import product

app = FastAPI(title="backend-Country-API")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "API connected to Supabase DB!"}


app.include_router(product.router)
