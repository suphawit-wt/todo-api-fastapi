from fastapi import APIRouter

from todo_api.api.endpoints import auth, todos

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(todos.router, prefix="/todos", tags=["Todos"])
