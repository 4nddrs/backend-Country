from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import task as crud_task
from app.schemas import task as schemas_task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=schemas_task.Task, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: schemas_task.TaskCreate):
    task = await crud_task.create_task(task_in)
    if not task:
        raise HTTPException(status_code=400, detail="Task could not be created")
    return task


@router.get("/", response_model=List[schemas_task.Task])
async def list_tasks(skip: int = 0, limit: int = 100):
    tasks = await crud_task.get_tasks(skip=skip, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=schemas_task.Task)
async def get_task(task_id: int):
    task = await crud_task.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=schemas_task.Task)
async def update_task(task_id: int, task_in: schemas_task.TaskUpdate):
    updated_task = await crud_task.update_task(task_id, task_in)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}", response_model=schemas_task.Task)
async def delete_task(task_id: int):
    deleted_task = await crud_task.delete_task(task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
