# app/supabase_client.py
from supabase import acreate_client, AsyncClient
from app.config import SUPABASE_URL, SUPABASE_KEY  # ✅ importar de tu config.py
import asyncio

supabase: AsyncClient = None

async def get_supabase() -> AsyncClient:
    global supabase
    if supabase is None:
        supabase = await acreate_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase
