from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


# === BASE ===
class HorseAssignmentBase(BaseModel):
    assignmentDate: date
    endDate: date
    fk_idEmployee: int
    fk_idHorse: int


class HorseAssignmentCreate(HorseAssignmentBase):
    pass


# ⚠️ En update los campos deben ser opcionales para permitir actualizaciones parciales
class HorseAssignmentUpdate(BaseModel):
    assignmentDate: Optional[date] = None
    endDate: Optional[date] = None
    fk_idEmployee: Optional[int] = None
    fk_idHorse: Optional[int] = None


# === MODELOS ANIDADOS (JOIN) ===
class Position(BaseModel):
    idPositionEmployee: int
    namePosition: str


class EmployeeMini(BaseModel):
    idEmployee: int
    fullName: str
    fk_idPositionEmployee: Optional[int]
    employee_position: Optional[Position] = None


class HorseMini(BaseModel):
    idHorse: int
    horseName: str
    state: str


# === MODELOS DE RESPUESTA ===
class HorseAssignmentInDBBase(BaseModel):
    idHorseAssignments: int
    assignmentDate: date
    endDate: date
    fk_idEmployee: Optional[int] = None
    fk_idHorse: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HorseAssignment(HorseAssignmentInDBBase):
    """Modelo estándar (CRUD básico)"""
    pass


class HorseAssignmentWithDetails(HorseAssignmentInDBBase):
    """Modelo extendido para /with_details"""
    horse: Optional[HorseMini] = None
    employee: Optional[EmployeeMini] = None
