from typing import Sequence

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from todo_api.models.todo import Todo
from todo_api.repositories.base_repository import BaseRepository


class TodoRepository(BaseRepository[Todo]):
    def __init__(self, db: AsyncSession):
        super().__init__(Todo, db)

    async def get_all_by_user_id(self, user_id: int) -> Sequence[Todo]:
        result = await self._db.execute(
            select(self._model)
            .filter_by(user_id=user_id)
            .order_by(desc(self._model.id))
        )
        return result.scalars().all()
