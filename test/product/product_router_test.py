from decimal import Decimal
from http import HTTPStatus

import pytest
from httpx import AsyncClient

from conftest import (
    STANDARD_NAME,
    NONEXISTENT_ID,
    STANDARD_PRICE_IN_CENTS,
)
from product.conftest import (
    assert_standard_product_from_dict,
    assert_product_not_found_from_dict,
)
from product.product_model import ProductModel

pytestmark = pytest.mark.asyncio


async def test_1_get_all_products_router(async_client: AsyncClient) -> None:
    """
    Verifies that ``GET /product/`` returns ``200 OK`` and an empty list when no products exist.

    :raises AssertionError: If the status code or response body are unexpected.
    """
    response = await async_client.get(url="/product/")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0


async def test_2_get_all_products_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """
    Verifies that ``GET /product/`` returns ``200 OK`` and exactly one product after a single
    product has been created, and that the product matches the standard fixtures.

    :raises AssertionError: If the status code, list length, or product data are unexpected.
    """
    response = await async_client.get(url="/product/")
    all_products = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(all_products) == 1
    assert_standard_product_from_dict(all_products[0])


async def test_1_get_some_products_router(async_client: AsyncClient) -> None:
    """
    Verifies that ``GET /product/some`` returns ``200 OK`` and an empty list when both
    ``begin`` and ``end`` are ``0``.

    :raises AssertionError: If the status code or response body are unexpected.
    """
    response = await async_client.get(url="/product/some", params={"begin": 0, "end": 0})

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0


async def test_2_get_some_products_router(async_client: AsyncClient) -> None:
    """
    Verifies that ``GET /product/some`` returns ``200 OK`` and an empty list when ``begin``
    is ``0`` and ``end`` is the current maximum ID (or ``INT_MAX`` when the table is empty),
    i.e. the range contains no valid lower bound.

    :raises AssertionError: If the status code or response body are unexpected.
    """
    record_with_max_id = await ProductModel.all().order_by("-id").first()
    max_id = record_with_max_id.id if record_with_max_id else 2_147_483_647

    response = await async_client.get(url="/product/some", params={"begin": 0, "end": max_id})

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0


async def test_3_get_some_products_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """
    Verifies that ``GET /product/some`` returns ``200 OK`` and an empty list when the range
    ``(0, 0)`` is requested even after a product has been created, since no product
    can have an ID of ``0``.

    :raises AssertionError: If the status code or response body are unexpected.
    """
    response = await async_client.get(url="/product/some", params={"begin": 0, "end": 0})

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0


async def test_4_get_some_products_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """
    Verifies that ``GET /product/some`` returns ``200 OK`` and exactly the created product
    when the range ``[product.id, product.id + 1)`` is requested.

    :raises AssertionError: If the status code, list length, or product data are unexpected.
    """
    response = await async_client.get(
        url="/product/some",
        params={"begin": standard_product.id, "end": standard_product.id + 1},
    )
    some_products = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(some_products) == 1
    assert_standard_product_from_dict(some_products[0])


async def test_1_get_product_by_id_router(async_client: AsyncClient) -> None:
    """
    Verifies that ``GET /product/{id}`` returns ``404 NOT_FOUND`` with the expected error
    payload when a product with ID ``0`` (non-existent) is requested.

    :raises AssertionError: If the status code or error payload are unexpected.
    """
    response = await async_client.get(url=f"/product/{NONEXISTENT_ID}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert_product_not_found_from_dict(NONEXISTENT_ID, response.json())


async def test_2_get_product_by_id_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """
    Verifies that ``GET /product/{id}`` returns ``200 OK`` and a product matching the
    standard fixtures when an existing product ID is requested.

    :raises AssertionError: If the status code or product data are unexpected.
    """
    response = await async_client.get(url=f"/product/{standard_product.id}")

    assert response.status_code == HTTPStatus.OK
    assert_standard_product_from_dict(response.json())


async def test_1_create_product_router(async_client: AsyncClient) -> None:
    """
    Verifies that ``POST /product/`` returns ``200 OK`` and a product matching the standard
    fixtures when a valid request body is supplied.

    :raises AssertionError: If the status code or created product data are unexpected.
    """
    response = await async_client.post(
        url="/product/",
        json={"name": STANDARD_NAME, "price_in_cents": str(STANDARD_PRICE_IN_CENTS)},
    )

    assert response.status_code == HTTPStatus.OK
    assert_standard_product_from_dict(response.json())


async def test_2_create_product_router(async_client: AsyncClient) -> None:
    """
    Verifies that ``POST /product/`` returns ``422 UNPROCESSABLE_CONTENT`` with a
    ``string_type`` validation error when ``name`` is an integer instead of a string.

    :raises AssertionError: If the status code or validation error details are unexpected.
    """
    wrong_name = 1
    response = await async_client.post(
        url="/product/",
        json={"name": wrong_name, "price_in_cents": str(STANDARD_PRICE_IN_CENTS)},
    )
    error = response.json()["detail"][0]

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert error["type"] == "string_type"
    assert error["loc"] == ["body", "name"]
    assert error["msg"] == "Input should be a valid string"
    assert error["input"] == wrong_name


async def test_3_create_product_router(async_client: AsyncClient) -> None:
    """
    Verifies that ``POST /product/`` returns ``422 UNPROCESSABLE_CONTENT`` with a
    ``decimal_parsing`` validation error when ``price_in_cents`` is an empty string.

    :raises AssertionError: If the status code or validation error details are unexpected.
    """
    wrong_price_in_cents = ""
    response = await async_client.post(
        url="/product/",
        json={"name": STANDARD_NAME, "price_in_cents": wrong_price_in_cents},
    )
    error = response.json()["detail"][0]

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert error["type"] == "decimal_parsing"
    assert error["loc"] == ["body", "price_in_cents"]
    assert error["msg"] == "Input should be a valid decimal"
    assert error["input"] == wrong_price_in_cents


async def test_1_update_product_router(async_client: AsyncClient) -> None:
    """
    Verifies that ``PATCH /product/{id}`` returns ``404 NOT_FOUND`` with the expected error
    payload when attempting to update a product with ID ``0`` (non-existent).

    :raises AssertionError: If the status code or error payload are unexpected.
    """
    response = await async_client.patch(
        url=f"/product/{NONEXISTENT_ID}",
        json={"name": STANDARD_NAME, "price_in_cents": str(STANDARD_PRICE_IN_CENTS)},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert_product_not_found_from_dict(NONEXISTENT_ID, response.json())


async def test_2_update_product_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """
    Verifies that ``PATCH /product/{id}`` returns ``422 UNPROCESSABLE_CONTENT`` with a
    ``string_type`` validation error when ``name`` is an integer, even when the target
    product exists.

    :raises AssertionError: If the status code or validation error details are unexpected.
    """
    wrong_name = 1
    response = await async_client.patch(
        url=f"/product/{standard_product.id}",
        json={"name": wrong_name, "price_in_cents": str(STANDARD_PRICE_IN_CENTS)},
    )
    error = response.json()["detail"][0]

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert error["type"] == "string_type"
    assert error["loc"] == ["body", "name"]
    assert error["msg"] == "Input should be a valid string"
    assert error["input"] == wrong_name


async def test_3_update_product_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """
    Verifies that ``PATCH /product/{id}`` returns ``422 UNPROCESSABLE_CONTENT`` with a
    ``decimal_parsing`` validation error when ``price_in_cents`` is an empty string, even
    when the target product exists.

    :raises AssertionError: If the status code or validation error details are unexpected.
    """
    wrong_price_in_cents = ""
    response = await async_client.patch(
        url=f"/product/{standard_product.id}",
        json={"name": STANDARD_NAME, "price_in_cents": wrong_price_in_cents},
    )
    error = response.json()["detail"][0]

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert error["type"] == "decimal_parsing"
    assert error["loc"] == ["body", "price_in_cents"]
    assert error["msg"] == "Input should be a valid decimal"
    assert error["input"] == wrong_price_in_cents


async def test_4_update_product_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """
    Verifies that ``PATCH /product/{id}`` returns ``200 OK`` and correctly persists new
    values when a valid request body is supplied for an existing product.

    The updated ``name`` should have the ``_updated`` suffix and ``price_in_cents`` should
    be incremented by ``10`` compared to the standard fixture.

    :raises AssertionError: If the status code or updated product fields are unexpected.
    """
    updated_name = STANDARD_NAME + "_updated"
    updated_price_in_cents = STANDARD_PRICE_IN_CENTS + Decimal("10")
    response = await async_client.patch(
        url=f"/product/{standard_product.id}",
        json={"name": updated_name, "price_in_cents": str(updated_price_in_cents)},
    )
    updated_product = response.json()

    assert response.status_code == HTTPStatus.OK
    assert updated_product["name"] == updated_name
    assert Decimal(str(updated_product["price_in_cents"])) == updated_price_in_cents


async def test_1_delete_product_router(async_client: AsyncClient) -> None:
    """
    Verifies that ``DELETE /product/{id}`` returns ``404 NOT_FOUND`` with the expected error
    payload when attempting to delete a product with ID ``0`` (non-existent).

    :raises AssertionError: If the status code or error payload are unexpected.
    """
    response = await async_client.delete(url=f"/product/{NONEXISTENT_ID}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert_product_not_found_from_dict(NONEXISTENT_ID, response.json())


async def test_2_delete_product_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """
    Verifies that ``DELETE /product/{id}`` returns ``204 NO_CONTENT`` after successfully
    deleting an existing product.

    :raises AssertionError: If the status code is unexpected.
    """
    response = await async_client.delete(url=f"/product/{standard_product.id}")

    assert response.status_code == HTTPStatus.NO_CONTENT
