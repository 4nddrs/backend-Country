from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import application_procedure as crud_app_proc
from app.schemas import application_procedure as schemas_app_proc

router = APIRouter(prefix="/application_procedures", tags=["application_procedures"])


@router.post(
    "/",
    response_model=schemas_app_proc.ApplicationProcedure,
    status_code=status.HTTP_201_CREATED,
)
async def create_app_proc(proc_in: schemas_app_proc.ApplicationProcedureCreate):
    proc = await crud_app_proc.create_application_procedure(proc_in)
    if not proc:
        raise HTTPException(
            status_code=400, detail="Application procedure could not be created"
        )
    return proc


@router.get("/", response_model=List[schemas_app_proc.ApplicationProcedure])
async def list_app_procs(skip: int = 0, limit: int = 100):
    procs = await crud_app_proc.get_application_procedures(skip=skip, limit=limit)
    return procs


@router.get("/{proc_id}", response_model=schemas_app_proc.ApplicationProcedure)
async def get_app_proc(proc_id: int):
    proc = await crud_app_proc.get_application_procedure(proc_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Application procedure not found")
    return proc


@router.put("/{proc_id}", response_model=schemas_app_proc.ApplicationProcedure)
async def update_app_proc(
    proc_id: int, proc_in: schemas_app_proc.ApplicationProcedureUpdate
):
    updated_proc = await crud_app_proc.update_application_procedure(proc_id, proc_in)
    if not updated_proc:
        raise HTTPException(status_code=404, detail="Application procedure not found")
    return updated_proc


@router.delete("/{proc_id}", response_model=schemas_app_proc.ApplicationProcedure)
async def delete_app_proc(proc_id: int):
    deleted_proc = await crud_app_proc.delete_application_procedure(proc_id)
    if not deleted_proc:
        raise HTTPException(status_code=404, detail="Application procedure not found")
    return deleted_proc
