from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import task_category as crud_category
from app.schemas import task_category as schemas_category

router = APIRouter(prefix="/task-categories", tags=["task-categories"])


@router.post(
    "/",
    response_model=schemas_category.TaskCategory,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_category(category_in: schemas_category.TaskCategoryCreate):
    category = await crud_category.create_task_category(category_in)
    if not category:
        raise HTTPException(
            status_code=400, detail="Task category could not be created"
        )
    return category


@router.get("/", response_model=List[schemas_category.TaskCategory])
async def list_task_categories(skip: int = 0, limit: int = 100):
    categories = await crud_category.get_task_categories(skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=schemas_category.TaskCategory)
async def get_task_category(category_id: int):
    category = await crud_category.get_task_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Task category not found")
    return category


@router.put("/{category_id}", response_model=schemas_category.TaskCategory)
async def update_task_category(
    category_id: int, category_in: schemas_category.TaskCategoryUpdate
):
    updated_category = await crud_category.update_task_category(
        category_id, category_in
    )
    if not updated_category:
        raise HTTPException(status_code=404, detail="Task category not found")
    return updated_category


@router.delete("/{category_id}", response_model=schemas_category.TaskCategory)
async def delete_task_category(category_id: int):
    deleted_category = await crud_category.delete_task_category(category_id)
    if not deleted_category:
        raise HTTPException(status_code=404, detail="Task category not found")
    return deleted_category
