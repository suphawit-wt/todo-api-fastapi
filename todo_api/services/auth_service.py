from dataclasses import dataclass
from typing import Optional

from todo_api.core.exceptions import UnauthorizedError, UnexpectedError
from todo_api.core.security import (
    UserRole,
    generate_access_token,
    hash_password,
    validate_password,
)
from todo_api.models.user import User
from todo_api.repositories.user_repository import UserRepository
from todo_api.schemas.request.login_request import LoginRequest
from todo_api.schemas.request.register_request import RegisterRequest
from todo_api.schemas.response.token_response import TokenResponse


@dataclass
class AuthService:
    user_repo: UserRepository

    async def login(self, req: LoginRequest) -> TokenResponse:
        user: Optional[User] = await self.user_repo.get_by_username(req.username)
        if not user:
            raise UnauthorizedError("Invalid username or password")
        if not validate_password(req.password, user.password):
            raise UnauthorizedError("Invalid username or password")

        access_token: str = generate_access_token(user.id, UserRole.USER)
        return TokenResponse(access_token=access_token)

    async def register(self, req: RegisterRequest) -> None:
        user: User = User(
            username=req.username,
            email=req.email,
            password=hash_password(req.password),
            first_name=req.first_name,
            last_name=req.last_name,
        )

        created_user: User = await self.user_repo.create(user)
        if not created_user:
            raise UnexpectedError()
