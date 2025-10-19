from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class MedicineBase(BaseModel):
    name: str
    description: Optional[str] = None
    medicationType: Optional[str] = None
    stock: int
    minStock: int
    boxExpirationDate: date
    expiryStatus: str
    stockStatus: str
    notifyDaysBefore: int
    isActive: Optional[bool] = None
    source: Optional[str] = None
    fk_idHorse: Optional[int] = None


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(MedicineBase):
    pass


class MedicineInDBBase(MedicineBase):
    idMedicine: int
    created_at: datetime

    class Config:
        from_attributes = True


class Medicine(MedicineInDBBase):
    pass
