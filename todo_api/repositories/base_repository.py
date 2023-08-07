from dataclasses import dataclass
from typing import Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from todo_api.core.exceptions import ConflictError

T = TypeVar("T")


@dataclass
class BaseRepository(Generic[T]):
    _model: Type[T]
    _db: AsyncSession

    async def get_all(self) -> Sequence[T]:
        result = await self._db.execute(
            select(self._model).order_by(desc(self._model.id))  # type: ignore
        )
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Optional[T]:
        result = await self._db.execute(select(self._model).filter_by(id=id))
        return result.scalars().first()

    async def create(self, obj_in: T) -> T:
        self._db.add(obj_in)
        try:
            await self._db.commit()
            await self._db.refresh(obj_in)
            return obj_in
        except IntegrityError as e:
            await self._db.rollback()
            if "ix_users_username" in str(e.orig):
                raise ConflictError("This Username already exists")
            elif "ix_users_email" in str(e.orig):
                raise ConflictError("This Email already exists")
            raise e

    async def update(self, obj_in: T) -> T:
        self._db.add(obj_in)
        try:
            await self._db.commit()
            await self._db.refresh(obj_in)
            return obj_in
        except IntegrityError as e:
            await self._db.rollback()
            if "ix_users_username" in str(e.orig):
                raise ConflictError("This Username already exists")
            elif "ix_users_email" in str(e.orig):
                raise ConflictError("This Email already exists")
            raise e

    async def delete(self, id: int) -> None:
        obj = await self.get_by_id(id)
        if obj:
            await self._db.delete(obj)
            await self._db.commit()
