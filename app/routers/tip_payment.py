from fastapi import APIRouter, HTTPException, status
from typing import List

from app.crud import tip_payment as crud_tip
from app.schemas import tip_payment as schemas_tip

router = APIRouter(prefix="/tip_payments", tags=["tip_payments"])


@router.post("/", response_model=schemas_tip.TipPayment, status_code=status.HTTP_201_CREATED)
async def create_tip_payment(tip_in: schemas_tip.TipPaymentCreate):
    created = await crud_tip.create_tip_payment(tip_in)
    if not created:
        raise HTTPException(status_code=400, detail="Tip payment could not be created")
    return created


@router.get("/", response_model=List[schemas_tip.TipPayment])
async def list_tip_payments(skip: int = 0, limit: int = 100):
    rows = await crud_tip.get_tip_payments(skip=skip, limit=limit)
    return rows


@router.get("/{tip_id}", response_model=schemas_tip.TipPayment)
async def get_tip_payment(tip_id: int):
    row = await crud_tip.get_tip_payment(tip_id)
    if not row:
        raise HTTPException(status_code=404, detail="Tip payment not found")
    return row


@router.put("/{tip_id}", response_model=schemas_tip.TipPayment)
async def update_tip_payment(tip_id: int, tip_in: schemas_tip.TipPaymentUpdate):
    updated = await crud_tip.update_tip_payment(tip_id, tip_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Tip payment not found")
    return updated


@router.delete("/{tip_id}", response_model=schemas_tip.TipPayment)
async def delete_tip_payment(tip_id: int):
    deleted = await crud_tip.delete_tip_payment(tip_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tip payment not found")
    return deleted
