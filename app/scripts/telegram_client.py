from __future__ import annotations

from typing import Any, Dict, Union

import httpx

from app.config import TELEGRAM_BOT_TOKEN

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


async def send_message(
    chat_id: Union[int, str],
    text: str,
    *,
    parse_mode: str = "HTML",
    timeout: float = 10.0,
) -> Dict[str, Any]:
    """
    Envía un mensaje a un chat de Telegram y valida la respuesta.

    Args:
        chat_id: Identificador del chat o usuario.
        text: Contenido del mensaje.
        parse_mode: Modo de formato (HTML por defecto).
        timeout: Tiempo máximo de espera en segundos.

    Returns:
        Respuesta JSON decodificada de la API de Telegram.

    Raises:
        RuntimeError: Si el token no está configurado o si la API responde con ok = False.
        httpx.RequestError / httpx.HTTPStatusError: Errores de red o HTTP.
    """
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN no configurado.")

    payload: Dict[str, Any] = {
        "chat_id": chat_id,
        "text": text,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(TELEGRAM_URL, json=payload)
        response.raise_for_status()

    data = response.json()
    if not data.get("ok", False):
        raise RuntimeError(f"Telegram API error: {data}")
    return data
