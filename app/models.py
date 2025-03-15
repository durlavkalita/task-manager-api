from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Task(Base):
  __tablename__ = "tasks"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True, nullable=False)
  description = Column(Text, nullable=True)
  status = Column(Text, default="pending", nullable=False)
  priority = Column(Integer, default=1, nullable=False)
  due_date = Column(DateTime, nullable=True)
  created_at = Column(DateTime, default=func.now(), nullable=False)

  owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Task ownership
  owner = relationship("User", back_populates="tasks")


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, nullable=False)
  email = Column(String, unique=True, nullable=False)
  password_hash = Column(String, nullable=False)
  role = Column(String, default="user", nullable=False)
  created_at = Column(DateTime, default=func.now(), nullable=False)
  
  # Relationship with tasks (One-to-Many)
  tasks = relationship("Task", back_populates="owner")