from todo_api.schemas.base_schema import BaseSchema


class TokenResponse(BaseSchema):
    access_token: str
