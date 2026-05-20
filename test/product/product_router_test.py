from decimal import Decimal
from http import HTTPStatus

import pytest
from httpx import AsyncClient

from constants import NONEXISTENT_ID
from product.product_asserts import (
    assert_standard_product_from_dict,
    assert_product_not_found_from_dict,
    assert_product_wrong_name,
    assert_product_wrong_price_in_cents,
    assert_product_wrong_user_access,
)
from product.product_model import ProductModel
from product_constants import (
    STANDARD_NAME,
    STANDARD_PRICE_IN_CENTS,
    STANDARD_USER_ACCESS,
    WRONG_NAME,
    WRONG_PRICE_IN_CENTS,
    WRONG_USER_ACCESS,
)
from user.user_access_enum import UserAccessEnum

pytestmark = pytest.mark.asyncio


async def test_1_get_all_products_router(async_client: AsyncClient) -> None:
    """GET /product/ returns 200 and an empty list when no products exist."""
    response = await async_client.get(url="/product/")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0


async def test_2_get_all_products_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """GET /product/ returns 200 and a single product matching the standard fixtures."""
    response = await async_client.get(url="/product/")
    all_products = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(all_products) == 1
    await assert_standard_product_from_dict(all_products[0])


async def test_1_get_some_products_router(async_client: AsyncClient) -> None:
    """GET /product/some returns 200 and an empty list when begin=0 and end=0."""
    response = await async_client.get(url="/product/some", params={"begin": 0, "end": 0})

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0


async def test_2_get_some_products_router(async_client: AsyncClient) -> None:
    """GET /product/some returns 200 and an empty list when begin=0 (no valid lower bound)."""
    record_with_max_id = await ProductModel.all().order_by("-id").first()
    max_id = record_with_max_id.id if record_with_max_id else 2_147_483_647

    response = await async_client.get(url="/product/some", params={"begin": 0, "end": max_id})

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0


async def test_3_get_some_products_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """GET /product/some returns 200 and an empty list for range (0, 0) even after a product is created."""
    response = await async_client.get(url="/product/some", params={"begin": 0, "end": 0})

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 0


async def test_4_get_some_products_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """GET /product/some returns 200 and the created product when its id is within the requested range."""
    response = await async_client.get(
        url="/product/some",
        params={"begin": standard_product.id, "end": standard_product.id + 1},
    )
    some_products = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(some_products) == 1
    await assert_standard_product_from_dict(some_products[0])


async def test_1_get_product_by_id_router(async_client: AsyncClient) -> None:
    """GET /product/{id} returns 404 with the expected payload for a non-existent id."""
    response = await async_client.get(url=f"/product/{NONEXISTENT_ID}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    await assert_product_not_found_from_dict(NONEXISTENT_ID, response.json())


async def test_2_get_product_by_id_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """GET /product/{id} returns 200 and a product matching the standard fixtures."""
    response = await async_client.get(url=f"/product/{standard_product.id}")

    assert response.status_code == HTTPStatus.OK
    await assert_standard_product_from_dict(response.json())


async def test_1_create_product_router(async_client: AsyncClient) -> None:
    """POST /product/ returns 200 and the created product when a valid body is supplied."""
    response = await async_client.post(
        url="/product/",
        json={
            "name": STANDARD_NAME,
            "price_in_cents": str(STANDARD_PRICE_IN_CENTS),
            "user_access": STANDARD_USER_ACCESS,
        },
    )

    assert response.status_code == HTTPStatus.OK
    await assert_standard_product_from_dict(response.json())


async def test_2_create_product_router(async_client: AsyncClient) -> None:
    """POST /product/ returns 422 with a string_type error when name is not a string."""
    response = await async_client.post(
        url="/product/",
        json={
            "name": WRONG_NAME,
            "price_in_cents": str(STANDARD_PRICE_IN_CENTS),
            "user_access": STANDARD_USER_ACCESS,
        },
    )

    await assert_product_wrong_name(response)


async def test_3_create_product_router(async_client: AsyncClient) -> None:
    """POST /product/ returns 422 with a decimal_parsing error when price_in_cents is invalid."""
    response = await async_client.post(
        url="/product/",
        json={
            "name": STANDARD_NAME,
            "price_in_cents": WRONG_PRICE_IN_CENTS,
            "user_access": STANDARD_USER_ACCESS,
        },
    )

    await assert_product_wrong_price_in_cents(response)


async def test_4_create_product_router(async_client: AsyncClient) -> None:
    """POST /product/ returns 422 with an enum error when user_access is invalid."""
    response = await async_client.post(
        url="/product/",
        json={
            "name": STANDARD_NAME,
            "price_in_cents": str(STANDARD_PRICE_IN_CENTS),
            "user_access": WRONG_USER_ACCESS,
        },
    )

    await assert_product_wrong_user_access(response)


async def test_1_update_product_router(async_client: AsyncClient) -> None:
    """PATCH /product/{id} returns 404 with the expected payload for a non-existent id."""
    response = await async_client.patch(
        url=f"/product/{NONEXISTENT_ID}",
        json={
            "name": STANDARD_NAME,
            "price_in_cents": str(STANDARD_PRICE_IN_CENTS),
            "user_access": STANDARD_USER_ACCESS,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    await assert_product_not_found_from_dict(NONEXISTENT_ID, response.json())


async def test_2_update_product_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """PATCH /product/{id} returns 422 with a string_type error when name is not a string."""
    response = await async_client.patch(
        url=f"/product/{standard_product.id}",
        json={
            "name": WRONG_NAME,
            "price_in_cents": str(STANDARD_PRICE_IN_CENTS),
            "user_access": STANDARD_USER_ACCESS,
        },
    )

    await assert_product_wrong_name(response)


async def test_3_update_product_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """PATCH /product/{id} returns 422 with a decimal_parsing error when price_in_cents is invalid."""
    response = await async_client.patch(
        url=f"/product/{standard_product.id}",
        json={
            "name": STANDARD_NAME,
            "price_in_cents": WRONG_PRICE_IN_CENTS,
            "user_access": STANDARD_USER_ACCESS,
        },
    )

    await assert_product_wrong_price_in_cents(response)


async def test_4_update_product_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """PATCH /product/{id} returns 422 with an enum error when user_access is invalid."""
    response = await async_client.patch(
        url=f"/product/{standard_product.id}",
        json={
            "name": STANDARD_NAME,
            "price_in_cents": str(STANDARD_PRICE_IN_CENTS),
            "user_access": WRONG_USER_ACCESS,
        },
    )

    await assert_product_wrong_user_access(response)


async def test_5_update_product_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """PATCH /product/{id} returns 200 and persists the updated fields correctly."""
    updated_name = STANDARD_NAME + "_updated"
    updated_price_in_cents = STANDARD_PRICE_IN_CENTS + Decimal("10")
    updated_user_access = UserAccessEnum.LOW

    response = await async_client.patch(
        url=f"/product/{standard_product.id}",
        json={
            "name": updated_name,
            "price_in_cents": str(updated_price_in_cents),
            "user_access": updated_user_access,
        },
    )
    updated_product = response.json()

    assert response.status_code == HTTPStatus.OK
    assert updated_product["name"] == updated_name
    assert Decimal(str(updated_product["price_in_cents"])) == updated_price_in_cents
    assert updated_product["user_access"] == updated_user_access


async def test_1_delete_product_router(async_client: AsyncClient) -> None:
    """DELETE /product/{id} returns 404 with the expected payload for a non-existent id."""
    response = await async_client.delete(url=f"/product/{NONEXISTENT_ID}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    await assert_product_not_found_from_dict(NONEXISTENT_ID, response.json())


async def test_2_delete_product_router(
        async_client: AsyncClient,
        standard_product: ProductModel,
) -> None:
    """DELETE /product/{id} returns 204 after successfully deleting an existing product."""
    response = await async_client.delete(url=f"/product/{standard_product.id}")

    assert response.status_code == HTTPStatus.NO_CONTENT
