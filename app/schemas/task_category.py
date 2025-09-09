from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskCategoryBase(BaseModel):
    categoryName: str
    description: Optional[str] = None


class TaskCategoryCreate(TaskCategoryBase):
    pass


class TaskCategoryUpdate(TaskCategoryBase):
    pass


class TaskCategoryInDBBase(TaskCategoryBase):
    idTaskCategory: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCategory(TaskCategoryInDBBase):
    pass
