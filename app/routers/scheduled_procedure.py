from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import scheduled_procedure as crud_proc
from app.schemas import scheduled_procedure as schemas_proc

router = APIRouter(prefix="/scheduled_procedures", tags=["scheduled_procedures"])


@router.post(
    "/",
    response_model=schemas_proc.ScheduledProcedure,
    status_code=status.HTTP_201_CREATED,
)
async def create_proc(proc_in: schemas_proc.ScheduledProcedureCreate):
    proc = await crud_proc.create_scheduled_procedure(proc_in)
    if not proc:
        raise HTTPException(
            status_code=400, detail="Scheduled procedure could not be created"
        )
    return proc


@router.get("/", response_model=List[schemas_proc.ScheduledProcedure])
async def list_procs(skip: int = 0, limit: int = 100):
    procs = await crud_proc.get_scheduled_procedures(skip=skip, limit=limit)
    return procs


@router.get("/{proc_id}", response_model=schemas_proc.ScheduledProcedure)
async def get_proc(proc_id: int):
    proc = await crud_proc.get_scheduled_procedure(proc_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Scheduled procedure not found")
    return proc


@router.put("/{proc_id}", response_model=schemas_proc.ScheduledProcedure)
async def update_proc(proc_id: int, proc_in: schemas_proc.ScheduledProcedureUpdate):
    updated_proc = await crud_proc.update_scheduled_procedure(proc_id, proc_in)
    if not updated_proc:
        raise HTTPException(status_code=404, detail="Scheduled procedure not found")
    return updated_proc


@router.delete("/{proc_id}", response_model=schemas_proc.ScheduledProcedure)
async def delete_proc(proc_id: int):
    deleted_proc = await crud_proc.delete_scheduled_procedure(proc_id)
    if not deleted_proc:
        raise HTTPException(status_code=404, detail="Scheduled procedure not found")
    return deleted_proc
