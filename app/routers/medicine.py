from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import medicine as crud_medicine
from app.schemas import medicine as schemas_medicine
from app.scripts.telegram_notifier import notificar_alertas_telegram

router = APIRouter(prefix="/medicines", tags=["Medicamentos"])

@router.post(
    "/", 
    response_model=schemas_medicine.Medicine, 
    status_code=status.HTTP_201_CREATED
)
async def create_medicine(medicine_in: schemas_medicine.MedicineCreate):
    try:
        medicine = await crud_medicine.create_medicine(medicine_in)
        if not medicine:
            raise HTTPException(status_code=400, detail="No se pudo crear el medicamento.")
        return medicine
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@router.get("/", response_model=List[schemas_medicine.Medicine])
async def list_medicines(skip: int = 0, limit: int = 100):
    medicines = await crud_medicine.get_medicines(skip=skip, limit=limit)
    return medicines

@router.get("/{medicine_id}", response_model=schemas_medicine.Medicine)
async def get_medicine(medicine_id: int):
    medicine = await crud_medicine.get_medicine(medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado.")
    return medicine

@router.put("/{medicine_id}", response_model=schemas_medicine.Medicine)
async def update_medicine(medicine_id: int, medicine_in: schemas_medicine.MedicineUpdate):
    updated_medicine = await crud_medicine.update_medicine(medicine_id, medicine_in)
    if not updated_medicine:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado o no actualizado.")
    return updated_medicine

@router.delete("/{medicine_id}", response_model=schemas_medicine.Medicine)
async def delete_medicine(medicine_id: int):
    deleted_medicine = await crud_medicine.delete_medicine(medicine_id)
    if not deleted_medicine:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado o ya eliminado.")
    return deleted_medicine


@router.post("/notify-expiring", tags=["Notificaciones"])
async def notify_expiring_medicines():
    """Prueba manual del envío de alertas de Telegram (medicamentos por vencer y stock bajo)."""
    try:
        await notificar_alertas_telegram()
        return {
            "status": "success",
            "message": "🔔 Notificaciones de Telegram ejecutadas manualmente. Revisa los chats de los administradores."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar notificaciones: {e}")
