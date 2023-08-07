from pydantic import EmailStr

from todo_api.schemas.base_schema import BaseSchema


class RegisterRequest(BaseSchema):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
