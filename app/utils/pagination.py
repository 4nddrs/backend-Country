import math
from typing import Any, Dict, List


def calculate_offset(page: int, limit: int) -> int:
    """
    Calcula el offset basado en una paginación 1-based.
    Levanta ValueError si los parámetros no son válidos.
    """
    if page < 1:
        raise ValueError("page debe ser mayor o igual a 1")
    if limit < 1:
        raise ValueError("limit debe ser mayor o igual a 1")
    return (page - 1) * limit


def build_paginated_response(
    items: List[Dict[str, Any]], total: int, page: int, limit: int
) -> Dict[str, Any]:
    total_items = total or 0
    total_pages = math.ceil(total_items / limit) if limit else 0
    return {
        "data": items,
        "total": total_items,
        "page": page,
        "limit": limit,
        "totalPages": total_pages,
    }
