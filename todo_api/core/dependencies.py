from typing import AsyncGenerator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from todo_api.core.database import AsyncDbSession
from todo_api.core.exceptions import DatabaseError, UnauthorizedError, UnexpectedError
from todo_api.core.security import auth_scheme, get_token_payload
from todo_api.repositories.todo_repository import TodoRepository
from todo_api.repositories.user_repository import UserRepository
from todo_api.services.auth_service import AuthService
from todo_api.services.todo_service import TodoService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncDbSession() as db:
        try:
            yield db
        except SQLAlchemyError:
            raise DatabaseError("Error establishing a database connection")
        finally:
            await db.close()


def get_user_id(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> int:
    if not token:
        raise UnauthorizedError("AccessToken is not provided")
    try:
        payload = get_token_payload(token.credentials)
        user_id: int = payload.get("sub")
        if not user_id:
            raise UnauthorizedError("AccessToken is invalid")
        return user_id
    except DecodeError:
        raise UnauthorizedError("AccessToken format is invalid")
    except ExpiredSignatureError:
        raise UnauthorizedError("AccessToken has expired")
    except InvalidTokenError:
        raise UnauthorizedError("AccessToken is invalid")
    except Exception:
        raise UnexpectedError()


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_todo_repository(db: AsyncSession = Depends(get_db)) -> TodoRepository:
    return TodoRepository(db)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repo)


def get_todo_service(
    todo_repo: TodoRepository = Depends(get_todo_repository),
) -> TodoService:
    return TodoService(todo_repo)
