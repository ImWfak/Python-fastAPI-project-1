from http import HTTPStatus

from _pytest._code import ExceptionInfo

from auth.auth_service import verify_password_service
from exception.app_exception import AppException
from exception.exeption_source_enum import ExceptionSourceEnum
from user.user_constants import (
    STANDARD_USERNAME,
    STANDARD_PASSWORD,
    STANDARD_USER_ACCESS,
)
from user.user_model import UserModel


async def assert_standard_user(user: UserModel) -> None:
    """Asserts that a user matches the standard test fixtures."""
    assert user.username == STANDARD_USERNAME
    assert await verify_password_service(STANDARD_PASSWORD, user.password)
    assert user.user_access == STANDARD_USER_ACCESS


async def assert_user_not_found_by_id(
        searchable_user_id: int,
        app_exception: ExceptionInfo[AppException],
) -> None:
    """Asserts that an AppException carries the expected 404 NOT_FOUND payload for a user id lookup."""
    exception_value = app_exception.value
    assert exception_value.message == f"User with id {searchable_user_id} not found"
    assert exception_value.exception_source == ExceptionSourceEnum.USER_SERVICE
    assert exception_value.http_status_code == HTTPStatus.NOT_FOUND


async def assert_user_not_found_by_username(
        searchable_username: str,
        app_exception: ExceptionInfo[AppException],
) -> None:
    """Asserts that an AppException carries the expected 404 NOT_FOUND payload for a username lookup."""
    exception_value = app_exception.value
    assert exception_value.message == f"User with username {searchable_username} not found"
    assert exception_value.exception_source == ExceptionSourceEnum.USER_SERVICE
    assert exception_value.http_status_code == HTTPStatus.NOT_FOUND


async def assert_username_already_exists(
        username: str,
        app_exception: ExceptionInfo[AppException],
) -> None:
    """Asserts that an AppException carries the expected 409 CONFLICT payload for a duplicate username."""
    exception_value = app_exception.value
    assert exception_value.message == f"User with username {username} already exists"
    assert exception_value.exception_source == ExceptionSourceEnum.USER_SERVICE
    assert exception_value.http_status_code == HTTPStatus.CONFLICT
