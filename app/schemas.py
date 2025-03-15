from pydantic import BaseModel, EmailStr
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

class UserCreate(BaseModel):
  username: str
  email: EmailStr
  password: str

class UserLogin(BaseModel):
  username: str
  password: str

class UserResponse(BaseModel):
  id: int
  username: str
  email: EmailStr
  role: str

  class Config:
      from_attributes = True