from decimal import Decimal
from http import HTTPStatus

from _pytest._code import ExceptionInfo

from exception.app_exception import AppException
from exception.exeption_source_enum import ExceptionSourceEnum
from product.product_constants import (
    STANDARD_NAME,
    STANDARD_PRICE_IN_CENTS,
    STANDARD_USER_ACCESS,
    WRONG_NAME,
    WRONG_PRICE_IN_CENTS,
    WRONG_USER_ACCESS
)
from product.product_model import ProductModel


async def assert_standard_product(product: ProductModel) -> None:
    """
    Asserts that a product matches the standard test fixtures.

    :param product: The :class:`ProductModel` instance to validate.
    :raises AssertionError: If ``name`` or ``price_in_cents`` do not match the standard values.
    """
    assert product.name == STANDARD_NAME
    assert product.price_in_cents == STANDARD_PRICE_IN_CENTS
    assert product.user_access == STANDARD_USER_ACCESS


async def assert_standard_product_from_dict(product_dict: dict) -> None:
    """
    Asserts that a product dictionary matches the standard test fixtures.

    :param product_dict: A dictionary representation of a product to validate.
    :raises AssertionError: If ``name`` or ``price_in_cents`` do not match the standard values.
    """
    assert product_dict.get("name") == STANDARD_NAME
    assert Decimal(str(product_dict.get("price_in_cents"))) == STANDARD_PRICE_IN_CENTS
    assert product_dict.get("user_access") == STANDARD_USER_ACCESS


async def assert_product_not_found(
        searchable_product_id: int,
        app_exception: ExceptionInfo[AppException],
) -> None:
    """
    Asserts that an :class:`AppException` carries the expected ``NOT_FOUND`` payload.

    :param searchable_product_id: The ID that was looked up, used to build the expected message.
    :param app_exception: The captured pytest exception info wrapping the :class:`AppException`.
    :raises AssertionError: If the exception message, source, or HTTP status code are unexpected.
    """
    exception_value = app_exception.value
    assert exception_value.message == f"Product with id {searchable_product_id} not found"
    assert exception_value.exception_source == ExceptionSourceEnum.PRODUCT_SERVICE
    assert exception_value.http_status_code == HTTPStatus.NOT_FOUND


async def assert_product_not_found_from_dict(
        searchable_product_id: int,
        app_exception_from_dict: dict,
) -> None:
    """
    Asserts that an exception dictionary carries the expected ``NOT_FOUND`` payload.

    :param searchable_product_id: The ID that was looked up, used to build the expected message.
    :param app_exception_from_dict: A dictionary representation of the exception to validate.
    :raises AssertionError: If the exception message or source do not match expected values.
    """
    assert app_exception_from_dict.get("message") == f"Product with id {searchable_product_id} not found"
    assert app_exception_from_dict.get("exception_source") == ExceptionSourceEnum.PRODUCT_SERVICE


async def assert_product_wrong_name(response: any) -> None:
    error = response.json()["detail"][0]

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert error["type"] == "string_type"
    assert error["loc"] == ["body", "name"]
    assert error["msg"] == "Input should be a valid string"
    assert error["input"] == WRONG_NAME


async def assert_product_wrong_price_in_cents(response: any) -> None:
    error = response.json()["detail"][0]

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert error["type"] == "decimal_parsing"
    assert error["loc"] == ["body", "price_in_cents"]
    assert error["msg"] == "Input should be a valid decimal"
    assert error["input"] == WRONG_PRICE_IN_CENTS


async def assert_product_wrong_user_access(response: any) -> None:
    error = response.json()["detail"][0]

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert error["type"] == "enum"
    assert error["loc"] == ["body", "user_access"]
    assert error["msg"] == "Input should be 'HIGH', 'MIDDLE' or 'LOW'"
    assert error["input"] == WRONG_USER_ACCESS
