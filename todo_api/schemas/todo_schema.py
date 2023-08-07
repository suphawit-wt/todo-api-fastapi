from todo_api.schemas.base_schema import BaseSchema


class TodoRequest(BaseSchema):
    title: str
    completed: bool = False


class TodoResponse(BaseSchema):
    id: int
    title: str
    completed: bool
    user_id: int
