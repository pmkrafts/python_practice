"""Generic repository pattern for SQLAlchemy models."""

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.core.exceptions import NotFoundException
from common.database.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class Repository(Generic[ModelT]):
    """Generic async CRUD repository."""

    def __init__(self, model: type[ModelT], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get(self, obj_id: str) -> ModelT:
        """Fetch a single record by primary key."""
        obj = await self.session.get(self.model, obj_id)
        if obj is None:
            raise NotFoundException(f"{self.model.__name__} with id={obj_id} not found")
        return obj

    async def list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelT]:
        """List records with pagination."""
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit),
        )
        return list(result.scalars().all())

    async def create(self, obj: ModelT) -> ModelT:
        """Persist a new record."""
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: ModelT) -> ModelT:
        """Update an existing record."""
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        """Hard-delete a record."""
        await self.session.delete(obj)
        await self.session.flush()

    async def soft_delete(self, obj_id: str) -> ModelT:
        """Soft-delete a record if it supports deleted_at."""
        obj = await self.get(obj_id)
        if hasattr(obj, "deleted_at"):
            from common.utils.datetime import utc_now

            obj.deleted_at = utc_now()
            await self.session.flush()
            await self.session.refresh(obj)
        else:
            await self.delete(obj)
        return obj
