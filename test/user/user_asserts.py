from http import HTTPStatus

from _pytest._code import ExceptionInfo

from exception.app_exception import AppException
from exception.exeption_source_enum import ExceptionSourceEnum
from user.user_constants import (
    STANDARD_USERNAME,
    STANDARD_PASSWORD,
    STANDARD_USER_ACCESS
)
from user.user_model import UserModel


async def assert_standard_user(user: UserModel) -> None:
    assert user.username == STANDARD_USERNAME
    assert user.password == STANDARD_PASSWORD
    assert user.user_access == STANDARD_USER_ACCESS


async def assert_user_not_found_by_id(
        searchable_user_id: int,
        app_exception: ExceptionInfo[AppException]
) -> None:
    exception_value = app_exception.value
    assert exception_value.message == f"User with id {searchable_user_id} not found"
    assert exception_value.exception_source == ExceptionSourceEnum.USER_SERVICE
    assert exception_value.http_status_code == HTTPStatus.NOT_FOUND


async def assert_user_not_found_by_username(
        searchable_username: str,
        app_exception: ExceptionInfo[AppException]
) -> None:
    exception_value = app_exception.value
    assert exception_value.message == f"User with username {searchable_username} not found"
    assert exception_value.exception_source == ExceptionSourceEnum.USER_SERVICE
    assert exception_value.http_status_code == HTTPStatus.NOT_FOUND


async def assert_username_already_exists(
        username: str,
        app_exception: ExceptionInfo[AppException]
) -> None:
    exception_value = app_exception.value
    assert exception_value.message == f"User with username {username} already exists"
    assert exception_value.exception_source == ExceptionSourceEnum.USER_SERVICE
    assert exception_value.http_status_code == HTTPStatus.CONFLICT
