from datetime import date, datetime
from fastapi import HTTPException
from app.supabase_client import get_supabase
from app.schemas.horse_assignment import HorseAssignmentCreate, HorseAssignmentUpdate


def serialize_horse_assignment(assignment: dict):
    """Convierte date/datetime a string para JSON"""
    data = assignment.copy()
    for key, value in data.items():
        if isinstance(value, (date, datetime)):
            data[key] = value.isoformat()
    return data


# 🔹 Obtener una asignación individual
async def get_horse_assignment(idHorseAssignments: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse_assignments")
        .select("*")
        .eq("idHorseAssignments", idHorseAssignments)
        .single()
        .execute()
    )
    return serialize_horse_assignment(result.data) if result.data else None


# 🔹 Obtener todas las asignaciones (sin detalles)
async def get_horse_assignments(skip: int = 0, limit: int = 100):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse_assignments")
        .select("*")
        .range(skip, skip + limit - 1)
        .execute()
    )
    return [serialize_horse_assignment(a) for a in result.data] if result.data else []


# 🔹 Crear asignación (validación estricta de rol)
async def create_horse_assignment(assignment: HorseAssignmentCreate):
    supabase = await get_supabase()
    assignment_dict = assignment.model_dump(mode="json")

    EXCLUDED_ROLES = {"secretaria", "administrador", "recepcionista"}

    # ✅ Obtener el empleado y su posición
    emp_res = (
        await supabase.table("employee")
        .select(
            """
            idEmployee,
            fullName,
            fk_idPositionEmployee,
            employee_position:fk_idPositionEmployee (
                namePosition
            )
            """
        )
        .eq("idEmployee", assignment.fk_idEmployee)
        .single()
        .execute()
    )

    employee = emp_res.data
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")

    # Normalizar y validar rol
    role_name = str(
        employee.get("employee_position", {}).get("namePosition", "")
    ).strip().lower()

    if role_name in EXCLUDED_ROLES:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede asignar a empleados con cargo '{role_name}'.",
        )

    # ✅ Verificar que el caballo existe y esté activo
    horse_res = (
        await supabase.table("horse")
        .select("idHorse, horseName, state")
        .eq("idHorse", assignment.fk_idHorse)
        .single()
        .execute()
    )
    horse = horse_res.data
    if not horse:
        raise HTTPException(status_code=404, detail="Caballo no encontrado.")
    if horse.get("state") in ["FALLECIDO", "AUSENTE"]:
        raise HTTPException(
            status_code=400,
            detail=f"El caballo '{horse.get('horseName')}' no está disponible para asignar.",
        )

    # ✅ Crear asignación
    result = await supabase.table("horse_assignments").insert(assignment_dict).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Error al crear la asignación.")

    return serialize_horse_assignment(result.data[0])


# 🔹 Actualizar asignación
async def update_horse_assignment(idHorseAssignments: int, assignment: HorseAssignmentUpdate):
    supabase = await get_supabase()
    assignment_dict = assignment.model_dump(mode="json", exclude_unset=True)

    result = (
        await supabase.table("horse_assignments")
        .update(assignment_dict)
        .eq("idHorseAssignments", idHorseAssignments)
        .execute()
    )
    return serialize_horse_assignment(result.data[0]) if result.data else None


# 🔹 Eliminar asignación
async def delete_horse_assignment(idHorseAssignments: int):
    supabase = await get_supabase()
    result = (
        await supabase.table("horse_assignments")
        .delete()
        .eq("idHorseAssignments", idHorseAssignments)
        .execute()
    )
    return serialize_horse_assignment(result.data[0]) if result.data else None


# 🔹 Obtener asignaciones con detalles (ya filtra roles/caballos inválidos)
async def get_horse_assignments_with_details():
    supabase = await get_supabase()
    result = (
        await supabase.table("horse_assignments")
        .select(
            """
            idHorseAssignments,
            assignmentDate,
            endDate,
            horse:fk_idHorse (
                idHorse,
                horseName,
                state
            ),
            employee:fk_idEmployee (
                idEmployee,
                fullName,
                fk_idPositionEmployee,
                employee_position:fk_idPositionEmployee (
                    idPositionEmployee,
                    namePosition
                )
            )
            """
        )
        .execute()
    )

    if not result.data:
        return []

    EXCLUDED_ROLES = {"secretaria", "administrador", "recepcionista"}

    filtered = []
    for a in result.data:
        horse = a.get("horse", {})
        employee = a.get("employee", {})
        emp_position = employee.get("employee_position", {})

        role_name = str(emp_position.get("namePosition", "")).strip().lower()

        # ❌ Saltar empleados no válidos
        if role_name in EXCLUDED_ROLES:
            continue

        # ❌ Saltar caballos no disponibles
        if horse and horse.get("state") in ["FALLECIDO", "AUSENTE"]:
            continue

        filtered.append(a)

    return [serialize_horse_assignment(a) for a in filtered]
