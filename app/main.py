from fastapi import FastAPI
from app.routes import task_routes, auth_routes
from app.database import engine, Base

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

# Include routes
app.include_router(task_routes.router)
app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "Task Management API is running!"}
