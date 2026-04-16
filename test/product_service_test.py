import pytest
from http import HTTPStatus
from decimal import Decimal
from pydantic import ValidationError
from _pytest._code import ExceptionInfo

from product.product_schema import (
    CreateProductSchema,
    UpdateProductSchema
)
from product.product_service import (
    get_all_products_service,
    get_some_products_service,
    get_product_by_id_service,
    create_product_service,
    update_product_service,
    delete_product_service
)
from common.app_exception import AppException
from product.product_model import ProductModel
from common.exeption_source_enum import ExceptionSourceEnum

STANDARD_NAME = "test name"
STANDARD_PRICE_IN_CENTS = Decimal(0)

pytestmark = pytest.mark.asyncio


async def create_standard_product() -> ProductModel:
    return await ProductModel.create(
        name=STANDARD_NAME,
        price_in_cents=STANDARD_PRICE_IN_CENTS
    )


async def standard_product_test(product: ProductModel) -> None:
    assert product.name == STANDARD_NAME
    assert product.price_in_cents == STANDARD_PRICE_IN_CENTS


async def standard_app_exception_not_found_test(
        searchable_product_id: int,
        app_exception: ExceptionInfo[AppException]
) -> None:
    app_exception_value = app_exception.value
    assert app_exception_value.message == f"Product with id {searchable_product_id} not found"
    assert app_exception_value.exception_source == ExceptionSourceEnum.PRODUCT_SERVICE
    assert app_exception_value.http_status_code == HTTPStatus.NOT_FOUND


###################################################################################################

async def test_1_get_all_products_service() -> None:
    """TEST OF GETTING LIST FROM EMPTY PRODUCT TABLE"""
    all_products: list[ProductModel] = await get_all_products_service()
    assert all_products.__len__() == 0


async def test_2_get_all_products_service() -> None:
    """TEST OF GETTING LIST FROM NOT EMPTY PRODUCT TABLE"""
    await create_standard_product()

    all_products: list[ProductModel] = await get_all_products_service()

    assert all_products.__len__() == 1
    await standard_product_test(all_products[0])


async def test_1_get_some_products_service() -> None:
    """TEST OF GETTING EMPTY LIST | FROM EMPTY PRODUCT TABLE"""
    all_products: list[ProductModel] = await get_some_products_service(0, 0)
    assert all_products.__len__() == 0


async def test_2_get_some_products_service() -> None:
    """TEST OF GETTING NOT EMPTY LIST | FROM EMPTY PRODUCT TABLE"""
    record_with_max_id = await ProductModel.all().order_by('-id').first()
    max_id = record_with_max_id.id if record_with_max_id else 2_147_483_647

    all_products: list[ProductModel] = await get_some_products_service(0, max_id)
    assert all_products.__len__() == 0


async def test_3_get_some_products_service() -> None:
    """TEST OF GETTING EMPTY LIST | FROM NOT EMPTY PRODUCT TABLE"""
    await create_standard_product()

    all_products: list[ProductModel] = await get_some_products_service(0, 0)
    assert all_products.__len__() == 0


async def test_4_get_some_products_service() -> None:
    """TEST OF GETTING NOT EMPTY LIST | FROM NOT EMPTY PRODUCT TABLE"""
    created_product: ProductModel = await create_standard_product()

    all_products: list[ProductModel] = await get_some_products_service(
        created_product.id,
        created_product.id + 1
    )

    assert all_products.__len__() == 1
    await standard_product_test(all_products[0])


async def test_1_get_product_by_id_service() -> None:
    """TEST OF GETTING NOT EXISTING PRODUCT"""
    id = 0

    with pytest.raises(AppException) as app_exception:
        await get_product_by_id_service(id)

    await standard_app_exception_not_found_test(id, app_exception)


async def test_2_get_product_by_id_service() -> None:
    """TEST OF GETTING EXISTING PRODUCT"""
    created_product: ProductModel = await create_standard_product()

    id = created_product.id

    found_product: ProductModel = await get_product_by_id_service(id)

    await standard_product_test(found_product)


async def test_1_create_product_service() -> None:
    """TEST OF CREATING PRODUCT SERVICE"""
    create_product_schema: CreateProductSchema = CreateProductSchema(
        name=STANDARD_NAME,
        price_in_cents=STANDARD_PRICE_IN_CENTS
    )

    created_product: ProductModel = await create_product_service(create_product_schema)

    await standard_product_test(created_product)


async def test_2_create_product_service() -> None:
    """TEST OF CREATING PRODUCT WITH WRONG NAME"""
    with pytest.raises(
            ValidationError,
            match="^1 validation error for CreateProductSchema\nname\\n\\s+Input should be a valid string "
                  + "\\[type=string_type, input_value=1, input_type=int\\]\\n\\s+For further information visit "
                  + "https://errors\\.pydantic\\.dev/2\\.12/v/string_type$"
    ):
        create_product_schema: CreateProductSchema = CreateProductSchema(
            name=1,
            price_in_cents=STANDARD_PRICE_IN_CENTS
        )

        await create_product_service(create_product_schema)


async def test_3_create_product_service() -> None:
    """TEST OF CREATING PRODUCT WITH WRONG PRICE_IN_CENTS"""
    with pytest.raises(
            ValidationError,
            match="^1 validation error for CreateProductSchema\nprice_in_cents\n\\s+Input should be a valid decimal "
                  + "\\[type=decimal_parsing, input_value='', input_type=str\\]\n\\s+For further information visit "
                  + "https://errors\\.pydantic\\.dev/2\\.12/v/decimal_parsing$"
    ):
        create_product_schema: CreateProductSchema = CreateProductSchema(
            name=STANDARD_NAME,
            price_in_cents=""
        )

        await create_product_service(create_product_schema)


async def test_1_update_product_service() -> None:
    """TEST OF UPDATING NOT EXISTING PRODUCT"""
    id = 0
    update_product_schema: UpdateProductSchema = UpdateProductSchema(
        name=STANDARD_NAME,
        price_in_cents=STANDARD_PRICE_IN_CENTS
    )

    with pytest.raises(AppException) as app_exception:
        await update_product_service(id, update_product_schema)

    await standard_app_exception_not_found_test(id, app_exception)


async def test_2_update_product_service() -> None:
    """TEST OF UPDATING PRODUCT WITH WRONG NAME"""
    created_product: ProductModel = await create_standard_product()

    with pytest.raises(
            ValidationError,
            match="^1 validation error for UpdateProductSchema\nname\n\\s+Input should be a valid string "
                  + "\\[type=string_type, input_value=\\d+, input_type=int\\]\n\\s+For further information visit "
                  + "https:\\/\\/errors\\.pydantic\\.dev\\/2\\.12\\/v\\/string_type$"
    ):
        update_product_schema: UpdateProductSchema = UpdateProductSchema(
            name=1,
            price_in_cents=STANDARD_PRICE_IN_CENTS
        )

        await update_product_service(created_product.id, update_product_schema)


async def test_3_update_product_service() -> None:
    """TEST OF UPDATING PRODUCT WITH WRONG PRICE_IN_CENTS"""
    created_product: ProductModel = await create_standard_product()

    with pytest.raises(
            ValidationError,
            match="^1 validation error for UpdateProductSchema\nprice_in_cents\n\\s+Input should be a valid decimal "
                  + "\\[type=decimal_parsing, input_value='', input_type=str\\]\n\\s+For further information visit "
                  + "https:\\/\\/errors\\.pydantic\\.dev\\/2\\.12\\/v\\/decimal_parsing$"
    ):
        update_product_schema: UpdateProductSchema = UpdateProductSchema(
            name=STANDARD_NAME,
            price_in_cents=""
        )

        await update_product_service(created_product.id, update_product_schema)


async def test_4_update_product_service() -> None:
    """TEST OF UPDATING PRODUCT"""
    created_product: ProductModel = await create_standard_product()

    update_product_schema: UpdateProductSchema = UpdateProductSchema(
        name=STANDARD_NAME + "_updated",
        price_in_cents=STANDARD_PRICE_IN_CENTS + Decimal(10)
    )

    updated_product: ProductModel = await update_product_service(created_product.id, update_product_schema)

    assert updated_product.name == STANDARD_NAME + "_updated"
    assert updated_product.price_in_cents == STANDARD_PRICE_IN_CENTS + Decimal(10)


async def test_1_delete_product_service() -> None:
    """TEST OF DELETING NOT EXISTING PRODUCT"""
    id = 0

    with pytest.raises(AppException) as app_exception:
        await delete_product_service(id)

    await standard_app_exception_not_found_test(id, app_exception)


async def test_2_delete_product_service() -> None:
    """TEST OF DELETING PRODUCT"""
    created_product: ProductModel = await create_standard_product()

    await delete_product_service(created_product.id)

    with pytest.raises(AppException) as app_exception:
        await get_product_by_id_service(created_product.id)

    await standard_app_exception_not_found_test(created_product.id, app_exception)
