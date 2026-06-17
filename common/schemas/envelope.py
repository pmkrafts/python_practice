"""Shared API response envelope schemas."""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiError(BaseModel):
    """Standard API error detail."""

    code: str
    message: str
    details: dict[str, str] | None = None


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response envelope."""

    success: bool
    data: T | None = None
    error: ApiError | None = None
    meta: dict[str, int | str | None] | None = None

    @classmethod
    def ok(cls, data: T, meta: dict[str, int | str | None] | None = None) -> "ApiResponse[T]":
        return cls(success=True, data=data, meta=meta)

    @classmethod
    def fail(
        cls,
        code: str,
        message: str,
        details: dict[str, str] | None = None,
    ) -> "ApiResponse[T]":
        return cls(
            success=False,
            error=ApiError(code=code, message=message, details=details),
        )
