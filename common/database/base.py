"""SQLAlchemy base models and mixins."""

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from common.utils.datetime import utc_now


class Base(DeclarativeBase):
    """Base declarative class for all ORM models."""

    type_annotation_map: dict[Any, Any] = {
        str: String(255),
    }


class UUIDMixin:
    """Mixin that adds a UUID primary key."""

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        default=utc_now,
        onupdate=utc_now,
    )


class SoftDeleteMixin:
    """Mixin that adds soft-delete support via deleted_at."""

    deleted_at: Mapped[datetime | None] = mapped_column(default=None)
