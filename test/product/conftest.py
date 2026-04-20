import pytest_asyncio
from http import HTTPStatus
from decimal import Decimal
from _pytest._code import ExceptionInfo

from common.app_exception import AppException
from product.product_model import ProductModel
from common.exeption_source_enum import ExceptionSourceEnum

STANDARD_NAME = "test name"
STANDARD_PRICE_IN_CENTS = Decimal(0)


@pytest_asyncio.fixture
async def standard_product() -> ProductModel:
    """
    Creates and returns a product with standard test fixtures.

    :returns: The newly created :class:`ProductModel` instance.
    """
    return await ProductModel.create(
        name=STANDARD_NAME,
        price_in_cents=STANDARD_PRICE_IN_CENTS
    )


async def assert_standard_product(product: ProductModel) -> None:
    """
    Asserts that a product matches the standard test fixtures.

    :param product: The :class:`ProductModel` instance to validate.
    :raises AssertionError: If ``name`` or ``price_in_cents`` do not match the standard values.
    """
    assert product.name == STANDARD_NAME
    assert product.price_in_cents == STANDARD_PRICE_IN_CENTS


async def assert_product_not_found(
        searchable_product_id: int,
        app_exception: ExceptionInfo[AppException]
) -> None:
    """
    Asserts that an :class:`AppException` carries the expected ``NOT_FOUND`` payload.

    :param searchable_product_id: The ID that was looked up, used to build the expected message.
    :param app_exception: The captured pytest exception info wrapping the :class:`AppException`.
    :raises AssertionError: If the exception message, source, or HTTP status code are unexpected.
    """
    app_exception_value = app_exception.value
    assert app_exception_value.message == f"Product with id {searchable_product_id} not found"
    assert app_exception_value.exception_source == ExceptionSourceEnum.PRODUCT_SERVICE
    assert app_exception_value.http_status_code == HTTPStatus.NOT_FOUND
