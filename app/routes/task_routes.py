from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas, database
from app.auth import admin_required, get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

limiter = Limiter(key_func=get_remote_address)

# Create Task
@router.post("/", response_model=schemas.TaskResponse)
@limiter.limit("5/minute")
def create_task(request: Request, task: schemas.TaskCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_task(db=db, task=task, current_user=current_user.id)

# Get Task by ID
@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    task = crud.get_task(db=db, task_id=task_id, current_user=current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Get All Tasks - Admin only route
@router.get("/", response_model=List[schemas.TaskResponse], dependencies=[Depends(admin_required)])
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_tasks(db=db, skip=skip, limit=limit)

# Update Task
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    updated_task = crud.update_task(db=db, task_id=task_id, task_update=task_update, current_user=current_user)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# Delete Task
@router.delete("/{task_id}", response_model=schemas.TaskResponse)
@limiter.limit("3/minute")
def delete_task(request: Request,task_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    deleted_task = crud.delete_task(db=db, task_id=task_id, current_user=current_user)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
