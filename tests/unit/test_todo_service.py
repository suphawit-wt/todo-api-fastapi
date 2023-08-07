from typing import List

import pytest
import pytest_asyncio

from todo_api.core.exceptions import AppException
from todo_api.models.todo import Todo
from todo_api.repositories.mock.todo_repository_mock import TodoRepositoryMock
from todo_api.repositories.todo_repository import TodoRepository
from todo_api.schemas.todo_schema import TodoRequest, TodoResponse
from todo_api.services.todo_service import TodoService


@pytest_asyncio.fixture
async def todo_repo() -> TodoRepositoryMock:
    return TodoRepositoryMock()


@pytest_asyncio.fixture
async def todo_service(todo_repo: TodoRepository) -> TodoService:
    return TodoService(todo_repo)


@pytest.mark.asyncio
async def test_get_todos(
    todo_service: TodoService, todo_repo: TodoRepositoryMock
) -> None:
    user_id: int = 1
    todo_create: Todo = Todo(id=1, title="Test Todo", completed=False, user_id=user_id)
    await todo_repo.create(todo_create)

    todos: List[TodoResponse] = await todo_service.get_todos(user_id)
    todos_mock: List[TodoResponse] = [TodoResponse.model_validate(todo_create)]

    assert todos == todos_mock


@pytest.mark.asyncio
async def test_create_todo_success(todo_service: TodoService) -> None:
    user_id: int = 1
    req = TodoRequest(title="Test Todo")
    todo: TodoResponse = await todo_service.create_todo(req, user_id)

    assert todo.title == req.title
    assert todo.completed == req.completed
    assert todo.user_id == user_id


@pytest.mark.asyncio
async def test_get_todo_by_id_success(
    todo_service: TodoService, todo_repo: TodoRepositoryMock
) -> None:
    user_id: int = 1
    todo_create: Todo = Todo(id=1, title="Test Todo", completed=False, user_id=user_id)
    await todo_repo.create(todo_create)

    todo_mock: TodoResponse = TodoResponse.model_validate(todo_create)
    todo: TodoResponse = await todo_service.get_todo_by_id(todo_mock.id, user_id)

    assert todo == todo_mock


@pytest.mark.asyncio
async def test_get_todo_by_id_not_found(todo_service: TodoService) -> None:
    user_id: int = 1
    non_exist_todo_id: int = 5000

    with pytest.raises(AppException) as ex:
        await todo_service.get_todo_by_id(non_exist_todo_id, user_id)

    assert ex.value.code == "NOT_FOUND"
    assert ex.value.status_code == 404
    assert ex.value.message == "Todo not found"


@pytest.mark.asyncio
async def test_get_todo_by_id_forbidden(
    todo_service: TodoService, todo_repo: TodoRepositoryMock
) -> None:
    user_id: int = 1
    other_user_id: int = 2
    todo: Todo = Todo(id=1, title="Test Todo", completed=False, user_id=other_user_id)
    await todo_repo.create(todo)

    with pytest.raises(AppException) as ex:
        await todo_service.get_todo_by_id(todo.id, user_id)

    assert ex.value.code == "FORBIDDEN"
    assert ex.value.status_code == 403
    assert ex.value.message == "You are not owner of this Todo"


@pytest.mark.asyncio
async def test_update_todo_success(
    todo_service: TodoService, todo_repo: TodoRepositoryMock
) -> None:
    user_id: int = 1
    todo_create: Todo = Todo(id=1, title="Test Todo", completed=False, user_id=user_id)
    await todo_repo.create(todo_create)

    todo_mock: TodoResponse = TodoResponse.model_validate(todo_create)
    req: TodoRequest = TodoRequest(title="Updated Todo", completed=True)
    todo_mock.title = req.title
    todo_mock.completed = req.completed

    todo: TodoResponse = await todo_service.update_todo(todo_mock.id, req, user_id)

    assert todo == todo_mock


@pytest.mark.asyncio
async def test_update_todo_not_found(todo_service: TodoService) -> None:
    user_id: int = 1
    non_exist_todo_id: int = 5000
    req: TodoRequest = TodoRequest(title="Updated Todo", completed=True)

    with pytest.raises(AppException) as ex:
        await todo_service.update_todo(non_exist_todo_id, req, user_id)

    assert ex.value.code == "NOT_FOUND"
    assert ex.value.status_code == 404
    assert ex.value.message == "Todo not found"


@pytest.mark.asyncio
async def test_update_todo_forbidden(
    todo_service: TodoService, todo_repo: TodoRepositoryMock
) -> None:
    user_id: int = 1
    other_user_id: int = 2
    todo: Todo = Todo(id=1, title="Test Todo", completed=False, user_id=other_user_id)
    await todo_repo.create(todo)

    req: TodoRequest = TodoRequest(title="Updated Todo", completed=True)
    with pytest.raises(AppException) as ex:
        await todo_service.update_todo(todo.id, req, user_id)

    assert ex.value.code == "FORBIDDEN"
    assert ex.value.status_code == 403
    assert ex.value.message == "You are not owner of this Todo"


@pytest.mark.asyncio
async def test_delete_todo_success(
    todo_service: TodoService, todo_repo: TodoRepositoryMock
) -> None:
    user_id: int = 1
    todo: Todo = Todo(id=1, title="Test Todo", completed=False, user_id=user_id)
    await todo_repo.create(todo)

    try:
        await todo_service.delete_todo(todo.id, user_id)
    except AppException as ex:
        pytest.fail(ex.message)


@pytest.mark.asyncio
async def test_delete_todo_not_found(todo_service: TodoService) -> None:
    user_id: int = 1
    non_exist_todo_id: int = 5000

    with pytest.raises(AppException) as ex:
        await todo_service.delete_todo(non_exist_todo_id, user_id)

    assert ex.value.code == "NOT_FOUND"
    assert ex.value.status_code == 404
    assert ex.value.message == "Todo not found"


@pytest.mark.asyncio
async def test_delete_todo_forbidden(
    todo_service: TodoService, todo_repo: TodoRepositoryMock
) -> None:
    user_id: int = 1
    todo: Todo = Todo(
        id=1, title="Test Todo", completed=False, user_id=user_id + 1  # Different user
    )
    await todo_repo.create(todo)

    with pytest.raises(AppException) as ex:
        await todo_service.delete_todo(todo.id, user_id)

    assert ex.value.code == "FORBIDDEN"
    assert ex.value.status_code == 403
    assert ex.value.message == "You are not owner of this Todo"
