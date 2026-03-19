"""
Main application module.

Initializes the FastAPI application and registers all routers.
This is the entry point of the API.
"""
from fastapi import FastAPI
from app.users.user_router import router as user_router
from app.task.task_router import router as task_router

app = FastAPI()

# Register application routers
app.include_router(user_router)
app.include_router(task_router)