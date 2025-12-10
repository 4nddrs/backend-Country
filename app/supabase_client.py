from supabase import acreate_client, create_client, AsyncClient, Client
from app.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
import asyncio

supabase: AsyncClient = None
supabase_admin: Client = None

async def get_supabase() -> AsyncClient:
    global supabase
    if supabase is None:
        supabase = await acreate_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase

def get_supabase_admin_client() -> Client:
   
    global supabase_admin
    if supabase_admin is None:
        supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    return supabase_admin