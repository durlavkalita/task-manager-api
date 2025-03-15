from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
  title: str
  description: Optional[str] = None
  status: Optional[str] = "pending"
  priority: Optional[int] = 1
  due_date: Optional[datetime]

class TaskCreate(TaskBase):
  pass

class TaskUpdate(TaskBase):
  pass

class TaskResponse(TaskBase):
  id: int
  created_at: datetime

  class Config:
    from_attributes = True