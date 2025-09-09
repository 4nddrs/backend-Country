from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class TaskBase(BaseModel):
    taskName: str
    description: Optional[str] = None
    assignmentDate: date
    completionDate: date
    taskStatus: str
    fk_idTaskCategory: int
    fk_idEmployee: Optional[int] = None  # Opcional ahora


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskInDBBase(TaskBase):
    idTask: int
    created_at: datetime

    class Config:
        from_attributes = True


class Task(TaskInDBBase):
    pass
