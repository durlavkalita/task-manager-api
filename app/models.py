from sqlalchemy import Column, Integer, String, Text, DateTime, func
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