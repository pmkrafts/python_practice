"""Smoke tests for shared common utilities."""

import pytest

from common.core.exceptions import (
    AppException,
    AuthException,
    ConflictException,
    NotFoundException,
    ValidationException,
)
from common.schemas.envelope import ApiResponse
from common.schemas.pagination import PaginatedResponse, PaginationParams
from common.utils.datetime import utc_now
from common.utils.hashing import get_password_hash, verify_password
from common.utils.id_generator import generate_uuid


def test_uuid_generation() -> None:
    uuid1 = generate_uuid()
    uuid2 = generate_uuid()
    assert isinstance(uuid1, str)
    assert len(uuid1) == 36
    assert uuid1 != uuid2


def test_password_hashing() -> None:
    password = "super-secret"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)


def test_utc_now() -> None:
    now = utc_now()
    assert now.tzinfo is not None


def test_pagination_params_defaults() -> None:
    params = PaginationParams()
    assert params.page == 1
    assert params.page_size == 20
    assert params.order == "desc"


def test_paginated_response_total_pages() -> None:
    response = PaginatedResponse.from_items(
        items=[1, 2, 3],
        total=10,
        page=1,
        page_size=3,
    )
    assert response.total == 10
    assert response.total_pages == 4


def test_api_response_ok() -> None:
    response = ApiResponse.ok(data={"id": 1})
    assert response.success is True
    assert response.data == {"id": 1}
    assert response.error is None


def test_api_response_fail() -> None:
    response = ApiResponse.fail(code="NOT_FOUND", message="Item not found")
    assert response.success is False
    assert response.error is not None
    assert response.error.code == "NOT_FOUND"


def test_exceptions() -> None:
    with pytest.raises(NotFoundException):
        raise NotFoundException()

    with pytest.raises(ValidationException):
        raise ValidationException()

    with pytest.raises(AuthException):
        raise AuthException()

    with pytest.raises(ConflictException):
        raise ConflictException()

    exc = AppException("Custom error", status_code=418)
    assert exc.status_code == 418
    assert exc.message == "Custom error"
