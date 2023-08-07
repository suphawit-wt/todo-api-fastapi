from todo_api.schemas.base_schema import BaseSchema


class LoginRequest(BaseSchema):
    username: str
    password: str
