import requests
from app.supabase_client import get_supabase

BOT_TOKEN = "8225256599:AAEWeT5H-LP069Gz631-1qBgDOyn6MwS5Zs"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

async def notificar_medicamento(nombre: str, stock: int, min_stock: int, fecha_venc, motivo: str):
    """
    Envía una notificación a todos los veterinarios (rol 8) con telegram_chat_id.
    motivo puede ser: 'stock' o 'vencimiento'
    """
    supabase = await get_supabase()

    # Buscar veterinarios con chat_id
    result = await supabase.table("erp_user").select("telegram_chat_id").eq("fk_idUserRole", 8).execute()
    veterinarios = [u["telegram_chat_id"] for u in result.data if u.get("telegram_chat_id")]

    if not veterinarios:
        print("⚠️ No hay veterinarios con chat_id registrado.")
        return

    if motivo == "stock":
        mensaje = (
            f"⚠️ *Alerta de Stock Bajo*\n"
            f"El medicamento *{nombre}* tiene stock bajo o agotado ({stock}/{min_stock})."
        )
    else:
        mensaje = (
            f"⚠️ *Alerta de Vencimiento*\n"
            f"El medicamento *{nombre}* está próximo a vencer el {fecha_venc}."
        )

    for chat_id in veterinarios:
        try:
            requests.post(
                f"{BASE_URL}/sendMessage",
                data={"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"},
                timeout=10,
            )
        except Exception as e:
            print(f"❌ Error enviando mensaje a {chat_id}: {e}")
