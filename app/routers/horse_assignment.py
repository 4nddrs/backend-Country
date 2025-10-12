from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import horse_assignment as crud_horse_assignment
from app.schemas import horse_assignment as schemas_horse_assignment

router = APIRouter(prefix="/horse_assignments", tags=["horse_assignments"])


# 🔹 Obtener asignaciones con detalles
@router.get(
    "/with_details",
    response_model=List[schemas_horse_assignment.HorseAssignmentWithDetails],
)
async def list_horse_assignments_with_details():
    data = await crud_horse_assignment.get_horse_assignments_with_details()
    return data or []


# 🔹 Crear una nueva asignación (con validaciones desde el CRUD)
@router.post(
    "/",
    response_model=schemas_horse_assignment.HorseAssignment,
    status_code=status.HTTP_201_CREATED,
)
async def create_horse_assignment(
    assignment_in: schemas_horse_assignment.HorseAssignmentCreate,
):
    assignment = await crud_horse_assignment.create_horse_assignment(assignment_in)
    if not assignment:
        raise HTTPException(status_code=400, detail="No se pudo crear la asignación.")
    return assignment


# 🔹 Listar asignaciones (sin detalles)
@router.get(
    "/",
    response_model=List[schemas_horse_assignment.HorseAssignment],
)
async def list_horse_assignments(skip: int = 0, limit: int = 100):
    return await crud_horse_assignment.get_horse_assignments(skip=skip, limit=limit)


# 🔹 Obtener una asignación por ID
@router.get(
    "/{assignment_id}",
    response_model=schemas_horse_assignment.HorseAssignment,
)
async def get_horse_assignment(assignment_id: int):
    assignment = await crud_horse_assignment.get_horse_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Asignación no encontrada.")
    return assignment


# 🔹 Actualizar asignación
@router.put(
    "/{assignment_id}",
    response_model=schemas_horse_assignment.HorseAssignment,
)
async def update_horse_assignment(
    assignment_id: int,
    assignment_in: schemas_horse_assignment.HorseAssignmentUpdate,
):
    updated_assignment = await crud_horse_assignment.update_horse_assignment(
        assignment_id, assignment_in
    )
    if not updated_assignment:
        raise HTTPException(status_code=404, detail="Asignación no encontrada.")
    return updated_assignment


# 🔹 Eliminar asignación
@router.delete(
    "/{assignment_id}",
    response_model=schemas_horse_assignment.HorseAssignment,
)
async def delete_horse_assignment(assignment_id: int):
    deleted_assignment = await crud_horse_assignment.delete_horse_assignment(
        assignment_id
    )
    if not deleted_assignment:
        raise HTTPException(status_code=404, detail="Asignación no encontrada.")
    return deleted_assignment
