from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from app.routes import task_routes, auth_routes
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

# Rate limiting middleware
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Limit request size to 1MB
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)

# Include routes
app.include_router(task_routes.router)
app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "Task Management API is running!"}
