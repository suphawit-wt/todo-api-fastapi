from typing import Any, Generic, Optional, TypeVar

from todo_api.schemas.base_schema import BaseSchema

T = TypeVar("T")


class ApiResponse(BaseSchema, Generic[T]):
    code: str = "SUCCESS"
    message: Optional[str] = None
    data: Optional[T] = None
    errors: Optional[Any] = None
