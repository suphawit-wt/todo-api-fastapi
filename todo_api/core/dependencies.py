from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from todo_api.core.database import AsyncDbSession
from todo_api.core.exceptions import DatabaseError


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncDbSession() as db:
        try:
            yield db
        except SQLAlchemyError:
            raise DatabaseError("Error establishing a database connection")
        finally:
            await db.close()
