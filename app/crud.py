from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

# Create Task
def create_task(db: Session, task: schemas.TaskCreate, user_id:int):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        owner_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Get Task by ID
def get_task(db: Session, task_id: int, current_user: models.User):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Allow access only if the user is admin or the task owner
    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this task")
    return task

# Get All Tasks (with optional filters)
def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()

# Update Task
def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate, current_user: models.User):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Only admin or owner can update
    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

# Delete Task
def delete_task(db: Session, task_id: int, current_user: models.User):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Only admin or owner can delete
    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    db.delete(task)
    db.commit()
    return task

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create User
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    print(user)
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role="user"
    )
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get User by Username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()