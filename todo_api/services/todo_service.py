from dataclasses import dataclass
from typing import List, Optional, Sequence

from todo_api.core.exceptions import ForbiddenError, NotFoundError
from todo_api.models.todo import Todo
from todo_api.repositories.todo_repository import TodoRepository
from todo_api.schemas.todo_schema import TodoRequest, TodoResponse


@dataclass
class TodoService:
    todo_repo: TodoRepository

    async def get_todos(self, user_id: int) -> List[TodoResponse]:
        todos: Sequence[Todo] = await self.todo_repo.get_all_by_user_id(user_id)
        return [TodoResponse.model_validate(todo) for todo in todos]

    async def get_todo_by_id(self, todo_id: int, user_id: int) -> TodoResponse:
        todo: Optional[Todo] = await self.todo_repo.get_by_id(todo_id)
        if not todo:
            raise NotFoundError("Todo not found")
        if todo.user_id != user_id:
            raise ForbiddenError("You are not owner of this Todo")

        return TodoResponse.model_validate(todo)

    async def create_todo(self, req: TodoRequest, user_id: int) -> TodoResponse:
        todo: Todo = Todo(**req.model_dump())
        todo.user_id = user_id
        created_todo: Todo = await self.todo_repo.create(todo)

        return TodoResponse.model_validate(created_todo)

    async def update_todo(
        self, todo_id: int, req: TodoRequest, user_id: int
    ) -> TodoResponse:
        todo: Optional[Todo] = await self.todo_repo.get_by_id(todo_id)
        if not todo:
            raise NotFoundError("Todo not found")
        if todo.user_id != user_id:
            raise ForbiddenError("You are not owner of this Todo")

        todo.title = req.title
        todo.completed = req.completed
        updated_todo: Todo = await self.todo_repo.update(todo)

        return TodoResponse.model_validate(updated_todo)

    async def delete_todo(self, todo_id: int, user_id: int) -> None:
        todo: Optional[Todo] = await self.todo_repo.get_by_id(todo_id)
        if not todo:
            raise NotFoundError("Todo not found")
        if todo.user_id != user_id:
            raise ForbiddenError("You are not owner of this Todo")

        await self.todo_repo.delete(todo_id)
