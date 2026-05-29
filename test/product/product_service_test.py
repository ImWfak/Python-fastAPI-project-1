import pytest
from pydantic import ValidationError

from exception.app_exception import AppException
from product.product_asserts import assert_standard_product, assert_product_not_found
from product.product_model import ProductModel
from product.product_schema import CreateProductSchema, UpdateProductSchema
from product.product_service import (
    get_all_products_service,
    get_some_products_service,
    get_product_by_id_service,
    create_product_service,
    update_product_by_id_service,
    delete_product_by_id_service,
)
from test_config import TestProductStandardValues, TestValidationRegexes

pytestmark = pytest.mark.asyncio


async def test_1_get_all_products_service() -> None:
    """Returns an empty list when no products exist."""
    all_products = await get_all_products_service()
    assert len(all_products) == 0


async def test_2_get_all_products_service(standard_product: ProductModel) -> None:
    """Returns a single product matching the standard fixtures after one is created."""
    all_products = await get_all_products_service()

    assert len(all_products) == 1
    await assert_standard_product(all_products[0])


async def test_1_get_some_products_service() -> None:
    """Returns an empty list when begin=0 and end=0."""
    some_products = await get_some_products_service(0, 0)
    assert len(some_products) == 0


async def test_2_get_some_products_service() -> None:
    """Returns an empty list when begin=0 (no valid lower bound)."""
    record_with_max_id = await ProductModel.all().order_by("-id").first()
    max_id = record_with_max_id.id if record_with_max_id else 2_147_483_647

    some_products = await get_some_products_service(0, max_id)
    assert len(some_products) == 0


async def test_3_get_some_products_service(standard_product: ProductModel) -> None:
    """Returns an empty list for range (0, 0) even after a product is created."""
    some_products = await get_some_products_service(0, 0)
    assert len(some_products) == 0


async def test_4_get_some_products_service(standard_product: ProductModel) -> None:
    """Returns exactly the created product when its id is within the requested range."""
    some_products = await get_some_products_service(
        standard_product.id,
        standard_product.id + 1,
    )

    assert len(some_products) == 1
    await assert_standard_product(some_products[0])


async def test_1_get_product_by_id_service() -> None:
    """Raises 404 AppException for a non-existent id."""
    with pytest.raises(AppException) as app_exception:
        await get_product_by_id_service(TestProductStandardValues.nonexistent_id)

    await assert_product_not_found(
        TestProductStandardValues.nonexistent_id,
        app_exception,
    )


async def test_2_get_product_by_id_service(standard_product: ProductModel) -> None:
    """Returns a product matching the standard fixtures for an existing id."""
    found_product = await get_product_by_id_service(standard_product.id)

    await assert_standard_product(found_product)


async def test_1_create_product_service() -> None:
    """Creates and returns a product matching the standard fixtures."""
    created_product = await create_product_service(CreateProductSchema(
        name=TestProductStandardValues.name,
        price_in_cents=TestProductStandardValues.price_in_cents,
        user_access=TestProductStandardValues.user_access,
    ))

    await assert_standard_product(created_product)


async def test_2_create_product_service() -> None:
    """Raises a string_type ValidationError when name is not a string."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for CreateProductSchema\nname\n\\s+{TestValidationRegexes.string_type_pattern}$",
    ):
        CreateProductSchema(
            name=TestProductStandardValues.wrong_type_name,
            price_in_cents=TestProductStandardValues.price_in_cents,
            user_access=TestProductStandardValues.user_access,
        )


async def test_3_create_product_service() -> None:
    """Raises a decimal_parsing ValidationError when price_in_cents is invalid."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for CreateProductSchema\nprice_in_cents\n\\s+{TestValidationRegexes.decimal_type_pattern}$",
    ):
        CreateProductSchema(
            name=TestProductStandardValues.name,
            price_in_cents=TestProductStandardValues.wrong_type_price_in_cents,
            user_access=TestProductStandardValues.user_access,
        )


async def test_4_create_product_service() -> None:
    """Raises an enum ValidationError when user_access is invalid."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for CreateProductSchema\nuser_access\n\\s+{TestValidationRegexes.enum_type_pattern}",
    ):
        CreateProductSchema(
            name=TestProductStandardValues.name,
            price_in_cents=TestProductStandardValues.price_in_cents,
            user_access=TestProductStandardValues.wrong_type_user_access,
        )


async def test_1_update_product_by_id_service() -> None:
    """Raises 404 AppException when attempting to update a non-existent product."""
    with pytest.raises(AppException) as app_exception:
        await update_product_by_id_service(
            TestProductStandardValues.nonexistent_id, UpdateProductSchema(
                name=TestProductStandardValues.updated_name,
                price_in_cents=TestProductStandardValues.updated_price_in_cents,
                user_access=TestProductStandardValues.updated_user_access,
        ))

    await assert_product_not_found(
        TestProductStandardValues.nonexistent_id,
        app_exception,
    )


async def test_2_update_product_by_id_service(standard_product: ProductModel) -> None:
    """Raises a string_type ValidationError when name is not a string."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for UpdateProductSchema\nname\n\\s+{TestValidationRegexes.string_type_pattern}$",
    ):
        UpdateProductSchema(
            name=TestProductStandardValues.wrong_type_name,
            price_in_cents=TestProductStandardValues.updated_price_in_cents,
            user_access=TestProductStandardValues.updated_user_access,
        )


async def test_3_update_product_by_id_service(standard_product: ProductModel) -> None:
    """Raises a decimal_parsing ValidationError when price_in_cents is invalid."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for UpdateProductSchema\nprice_in_cents\n\\s+{TestValidationRegexes.decimal_type_pattern}$",
    ):
        UpdateProductSchema(
            name=TestProductStandardValues.updated_name,
            price_in_cents=TestProductStandardValues.wrong_type_price_in_cents,
            user_access=TestProductStandardValues.updated_user_access,
        )


async def test_4_update_product_by_id_service(standard_product: ProductModel) -> None:
    """Raises an enum ValidationError when user_access is invalid."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for UpdateProductSchema\nuser_access\n\\s+{TestValidationRegexes.enum_type_pattern}",
    ):
        UpdateProductSchema(
            name=TestProductStandardValues.updated_name,
            price_in_cents=TestProductStandardValues.updated_price_in_cents,
            user_access=TestProductStandardValues.wrong_type_user_access,
        )


async def test_5_update_product_by_id_service(standard_product: ProductModel) -> None:
    """Correctly persists updated fields for an existing product."""
    updated_product = await update_product_by_id_service(
        standard_product.id,
        UpdateProductSchema(
            name=TestProductStandardValues.updated_name,
            price_in_cents=TestProductStandardValues.updated_price_in_cents,
            user_access=TestProductStandardValues.updated_user_access,
        ),
    )

    assert updated_product.name == TestProductStandardValues.updated_name
    assert updated_product.price_in_cents == TestProductStandardValues.updated_price_in_cents
    assert updated_product.user_access == TestProductStandardValues.updated_user_access


async def test_1_delete_product_by_id_service() -> None:
    """Raises 404 AppException when attempting to delete a non-existent product."""
    with pytest.raises(AppException) as app_exception:
        await delete_product_by_id_service(TestProductStandardValues.nonexistent_id)

    await assert_product_not_found(
        TestProductStandardValues.nonexistent_id,
        app_exception,
    )


async def test_2_delete_product_by_id_service(standard_product: ProductModel) -> None:
    """Deletes the product and confirms it is no longer retrievable."""
    id = standard_product.id

    await delete_product_by_id_service(id)

    assert await ProductModel.get_or_none(id=id) is None
