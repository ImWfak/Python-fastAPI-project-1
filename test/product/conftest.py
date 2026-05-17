from decimal import Decimal
from http import HTTPStatus

import pytest_asyncio
from _pytest._code import ExceptionInfo

from exception.app_exception import AppException
from exception.exeption_source_enum import ExceptionSourceEnum
from product.product_model import ProductModel
from user.user_access_enum import UserAccessEnum

NONEXISTENT_ID = 0
STANDARD_NAME = "test name"
STANDARD_PRICE_IN_CENTS = Decimal("0")
STANDARD_USER_ACCESS = UserAccessEnum.HIGH


@pytest_asyncio.fixture
async def standard_product() -> ProductModel:
    """
    Creates and returns a product with standard test fixtures.

    :returns: The newly created :class:`ProductModel` instance.
    """
    return await ProductModel.create(
        name=STANDARD_NAME,
        price_in_cents=STANDARD_PRICE_IN_CENTS,
        user_access=STANDARD_USER_ACCESS
    )


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
    exc = app_exception.value
    assert exc.message == f"Product with id {searchable_product_id} not found"
    assert exc.exception_source == ExceptionSourceEnum.PRODUCT_SERVICE
    assert exc.http_status_code == HTTPStatus.NOT_FOUND


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