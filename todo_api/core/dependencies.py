from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from todo_api.core.database import AsyncDbSession
from todo_api.core.exceptions import DatabaseError
from todo_api.repositories.todo_repository import TodoRepository
from todo_api.repositories.user_repository import UserRepository


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncDbSession() as db:
        try:
            yield db
        except SQLAlchemyError:
            raise DatabaseError("Error establishing a database connection")
        finally:
            await db.close()


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_todo_repository(db: AsyncSession = Depends(get_db)) -> TodoRepository:
    return TodoRepository(db)
