from dataclasses import dataclass, field
from typing import List, Optional, Sequence

from todo_api.models.todo import Todo


@dataclass
class TodoRepositoryMock:
    todos: List[Todo] = field(default_factory=list)
    next_id: int = 1

    async def get_all_by_user_id(self, user_id: int) -> Sequence[Todo]:
        return [todo for todo in self.todos if todo.user_id == user_id]

    async def get_by_id(self, todo_id: int) -> Optional[Todo]:
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    async def create(self, req: Todo) -> Todo:
        req.id = self.next_id
        self.todos.append(req)
        self.next_id += 1
        return req

    async def update(self, req: Todo) -> Todo:
        for i, todo in enumerate(self.todos):
            if todo.id == req.id:
                self.todos[i] = req
        return req

    async def delete(self, todo_id: int) -> None:
        todo: Optional[Todo] = await self.get_by_id(todo_id)
        if todo:
            self.todos.remove(todo)
