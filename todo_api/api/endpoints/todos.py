from typing import List

from fastapi import APIRouter, Depends

from todo_api.core.dependencies import get_todo_service, get_user_id
from todo_api.schemas.response.api_response import ApiResponse
from todo_api.schemas.todo_schema import TodoRequest, TodoResponse
from todo_api.services.todo_service import TodoService

router = APIRouter()


@router.get("/", response_model_exclude_none=True)
async def get_todos(
    todo_service: TodoService = Depends(get_todo_service),
    user_id: int = Depends(get_user_id),
) -> ApiResponse[List[TodoResponse]]:
    todos: List[TodoResponse] = await todo_service.get_todos(user_id)
    return ApiResponse[List[TodoResponse]](data=todos)


@router.get("/{todo_id}", response_model_exclude_none=True)
async def get_todo_by_id(
    todo_id: int,
    todo_service: TodoService = Depends(get_todo_service),
    user_id: int = Depends(get_user_id),
) -> ApiResponse[TodoResponse]:
    todo: TodoResponse = await todo_service.get_todo_by_id(todo_id, user_id)
    return ApiResponse[TodoResponse](data=todo)


@router.post("/", status_code=201, response_model_exclude_none=True)
async def create_todo(
    req: TodoRequest,
    todo_service: TodoService = Depends(get_todo_service),
    user_id: int = Depends(get_user_id),
) -> ApiResponse[TodoResponse]:
    todo: TodoResponse = await todo_service.create_todo(req, user_id)
    return ApiResponse[TodoResponse](data=todo)


@router.put("/{todo_id}", response_model_exclude_none=True)
async def update_todo(
    todo_id: int,
    req: TodoRequest,
    todo_service: TodoService = Depends(get_todo_service),
    user_id: int = Depends(get_user_id),
) -> ApiResponse[TodoResponse]:
    todo: TodoResponse = await todo_service.update_todo(todo_id, req, user_id)
    return ApiResponse[TodoResponse](data=todo)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: int,
    todo_service: TodoService = Depends(get_todo_service),
    user_id: int = Depends(get_user_id),
) -> None:
    await todo_service.delete_todo(todo_id, user_id)
