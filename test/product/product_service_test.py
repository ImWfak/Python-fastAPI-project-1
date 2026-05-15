from decimal import Decimal

import pytest
from pydantic import ValidationError

from exception.app_exception import AppException
from conftest import (
    STANDARD_NAME,
    NONEXISTENT_ID,
    STANDARD_PRICE_IN_CENTS,
)
from product.conftest import (
    assert_standard_product,
    assert_product_not_found,
)
from product.product_model import ProductModel
from product.product_schema import (
    CreateProductSchema,
    UpdateProductSchema,
)
from product.product_service import (
    get_all_products_service,
    get_some_products_service,
    get_product_by_id_service,
    create_product_service,
    update_product_service,
    delete_product_service,
)

pytestmark = pytest.mark.asyncio

_PYDANTIC_BASE_URL = r"https://errors\.pydantic\.dev/2\.12\/v"
_STRING_TYPE_PATTERN = (
        r"Input should be a valid string "
        r"\[type=string_type, input_value=.+, input_type=int\]\n"
        r"\s+For further information visit " + _PYDANTIC_BASE_URL + r"\/string_type"
)
_DECIMAL_PARSING_PATTERN = (
        r"Input should be a valid decimal "
        r"\[type=decimal_parsing, input_value='', input_type=str\]\n"
        r"\s+For further information visit " + _PYDANTIC_BASE_URL + r"\/decimal_parsing"
)


async def test_1_get_all_products_service() -> None:
    """
    Verifies that ``get_all_products_service`` returns an empty list when no products exist.

    :raises AssertionError: If the returned list is not empty.
    """
    all_products: list[ProductModel] = await get_all_products_service()
    assert len(all_products) == 0


async def test_2_get_all_products_service(standard_product: ProductModel) -> None:
    """
    Verifies that ``get_all_products_service`` returns exactly one product after a single product
    has been created, and that the product matches the standard fixtures.

    :raises AssertionError: If the list length is not 1 or the product data is unexpected.
    """
    all_products: list[ProductModel] = await get_all_products_service()

    assert len(all_products) == 1
    assert_standard_product(all_products[0])


async def test_1_get_some_products_service() -> None:
    """
    Verifies that ``get_some_products_service`` returns an empty list when both
    ``min_id`` and ``max_id`` are ``0``.

    :raises AssertionError: If the returned list is not empty.
    """
    some_products: list[ProductModel] = await get_some_products_service(0, 0)
    assert len(some_products) == 0


async def test_2_get_some_products_service() -> None:
    """
    Verifies that ``get_some_products_service`` returns an empty list when ``min_id`` is ``0``
    and ``max_id`` is set to the current maximum ID in the table (or ``INT_MAX`` when the
    table is empty), i.e. the range contains no valid lower bound.

    :raises AssertionError: If the returned list is not empty.
    """
    record_with_max_id = await ProductModel.all().order_by("-id").first()
    max_id = record_with_max_id.id if record_with_max_id else 2_147_483_647

    some_products: list[ProductModel] = await get_some_products_service(0, max_id)
    assert len(some_products) == 0


async def test_3_get_some_products_service(standard_product: ProductModel) -> None:
    """
    Verifies that ``get_some_products_service`` returns an empty list when the range
    ``(0, 0)`` is requested even after a product has been created, since no product
    can have an ID of ``0``.

    :raises AssertionError: If the returned list is not empty.
    """
    some_products: list[ProductModel] = await get_some_products_service(0, 0)
    assert len(some_products) == 0


async def test_4_get_some_products_service(standard_product: ProductModel) -> None:
    """
    Verifies that ``get_some_products_service`` returns exactly the created product when
    the range ``[product.id, product.id + 1)`` is requested.

    :raises AssertionError: If the list length is not 1 or the product data is unexpected.
    """
    some_products: list[ProductModel] = await get_some_products_service(
        standard_product.id,
        standard_product.id + 1,
    )

    assert len(some_products) == 1
    assert_standard_product(some_products[0])


async def test_1_get_product_by_id_service() -> None:
    """
    Verifies that ``get_product_by_id_service`` raises :class:`AppException` with
    ``NOT_FOUND`` when a product with ID ``0`` (non-existent) is requested.

    :raises AssertionError: If no exception is raised or the exception payload is unexpected.
    """
    with pytest.raises(AppException) as app_exception:
        await get_product_by_id_service(NONEXISTENT_ID)

    assert_product_not_found(NONEXISTENT_ID, app_exception)


async def test_2_get_product_by_id_service(standard_product: ProductModel) -> None:
    """
    Verifies that ``get_product_by_id_service`` successfully retrieves a product by its ID
    and that the returned data matches the standard fixtures.

    :raises AssertionError: If the product is not found or its data is unexpected.
    """
    found_product: ProductModel = await get_product_by_id_service(standard_product.id)

    assert_standard_product(found_product)


async def test_1_create_product_service() -> None:
    """
    Verifies that ``create_product_service`` successfully creates a product from a valid
    :class:`CreateProductSchema` and that the returned model matches the standard fixtures.

    :raises AssertionError: If the created product data is unexpected.
    """
    create_product_schema = CreateProductSchema(
        name=STANDARD_NAME,
        price_in_cents=STANDARD_PRICE_IN_CENTS,
    )
    created_product: ProductModel = await create_product_service(create_product_schema)

    assert_standard_product(created_product)


async def test_2_create_product_service() -> None:
    """
    Verifies that constructing a :class:`CreateProductSchema` with an integer ``name``
    raises a :class:`~pydantic.ValidationError` describing a ``string_type`` failure.

    :raises AssertionError: If no validation error is raised or the error message does not match.
    """
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for CreateProductSchema\nname\n\\s+{_STRING_TYPE_PATTERN}$",
    ):
        CreateProductSchema(name=1, price_in_cents=STANDARD_PRICE_IN_CENTS)


async def test_3_create_product_service() -> None:
    """
    Verifies that constructing a :class:`CreateProductSchema` with an empty string
    ``price_in_cents`` raises a :class:`~pydantic.ValidationError` describing a
    ``decimal_parsing`` failure.

    :raises AssertionError: If no validation error is raised or the error message does not match.
    """
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for CreateProductSchema\nprice_in_cents\n\\s+{_DECIMAL_PARSING_PATTERN}$",
    ):
        CreateProductSchema(name=STANDARD_NAME, price_in_cents="")


async def test_1_update_product_service() -> None:
    """
    Verifies that ``update_product_service`` raises :class:`AppException` with
    ``NOT_FOUND`` when attempting to update a product with ID ``0`` (non-existent).

    :raises AssertionError: If no exception is raised or the exception payload is unexpected.
    """
    update_product_schema = UpdateProductSchema(
        name=STANDARD_NAME,
        price_in_cents=STANDARD_PRICE_IN_CENTS,
    )

    with pytest.raises(AppException) as app_exception:
        await update_product_service(NONEXISTENT_ID, update_product_schema)

    assert_product_not_found(NONEXISTENT_ID, app_exception)


async def test_2_update_product_service(standard_product: ProductModel) -> None:
    """
    Verifies that constructing an :class:`UpdateProductSchema` with an integer ``name``
    raises a :class:`~pydantic.ValidationError` describing a ``string_type`` failure,
    even when the target product exists.

    :raises AssertionError: If no validation error is raised or the error message does not match.
    """
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for UpdateProductSchema\nname\n\\s+{_STRING_TYPE_PATTERN}$",
    ):
        UpdateProductSchema(name=1, price_in_cents=STANDARD_PRICE_IN_CENTS)


async def test_3_update_product_service(standard_product: ProductModel) -> None:
    """
    Verifies that constructing an :class:`UpdateProductSchema` with an empty string
    ``price_in_cents`` raises a :class:`~pydantic.ValidationError` describing a
    ``decimal_parsing`` failure, even when the target product exists.

    :raises AssertionError: If no validation error is raised or the error message does not match.
    """
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for UpdateProductSchema\nprice_in_cents\n\\s+{_DECIMAL_PARSING_PATTERN}$",
    ):
        UpdateProductSchema(name=STANDARD_NAME, price_in_cents="")


async def test_4_update_product_service(standard_product: ProductModel) -> None:
    """
    Verifies that ``update_product_service`` correctly persists new values when a valid
    :class:`UpdateProductSchema` is supplied for an existing product.

    The updated ``name`` should have the ``_updated`` suffix and ``price_in_cents``
    should be incremented by ``10`` compared to the standard fixture.

    :raises AssertionError: If the updated product fields do not reflect the new values.
    """
    updated_name = STANDARD_NAME + "_updated"
    updated_price_in_cents = STANDARD_PRICE_IN_CENTS + Decimal("10")
    update_product_schema = UpdateProductSchema(
        name=updated_name,
        price_in_cents=updated_price_in_cents,
    )
    updated_product: ProductModel = await update_product_service(standard_product.id, update_product_schema)

    assert updated_product.name == updated_name
    assert updated_product.price_in_cents == updated_price_in_cents


async def test_1_delete_product_service() -> None:
    """
    Verifies that ``delete_product_service`` raises :class:`AppException` with
    ``NOT_FOUND`` when attempting to delete a product with ID ``0`` (non-existent).

    :raises AssertionError: If no exception is raised or the exception payload is unexpected.
    """
    with pytest.raises(AppException) as app_exception:
        await delete_product_service(NONEXISTENT_ID)

    assert_product_not_found(NONEXISTENT_ID, app_exception)


async def test_2_delete_product_service(standard_product: ProductModel) -> None:
    """
    Verifies the full delete lifecycle: after ``delete_product_service`` is called for an
    existing product, a subsequent ``get_product_by_id_service`` call for the same ID
    raises :class:`AppException` with ``NOT_FOUND``.

    :raises AssertionError: If the product is still retrievable after deletion, or the
        exception payload on the follow-up lookup is unexpected.
    """
    await delete_product_service(standard_product.id)

    with pytest.raises(AppException) as app_exception:
        await get_product_by_id_service(standard_product.id)

    assert_product_not_found(standard_product.id, app_exception)
