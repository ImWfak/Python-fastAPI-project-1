from http import HTTPStatus

from exception.app_exception import AppException
from exception.exeption_source_enum import ExceptionSourceEnum
from product.product_model import ProductModel
from product.product_schema import CreateProductSchema, UpdateProductSchema


def _not_found(detail: str) -> AppException:
    return AppException(
        message=detail,
        exception_source=ExceptionSourceEnum.PRODUCT_SERVICE,
        http_status_code=HTTPStatus.NOT_FOUND,
    )


async def get_product_by_id(id: int) -> ProductModel:
    """Internal helper — raises 404 if the product does not exist."""
    if product := await ProductModel.get_or_none(id=id):
        return product
    raise _not_found(f"Product with id {id} not found")


async def get_all_products_service() -> list[ProductModel]:
    """Returns all products."""
    return await ProductModel.all()


async def get_some_products_service(begin: int, end: int) -> list[ProductModel]:
    """Returns all products whose id falls in the inclusive range [begin, end]."""
    return await ProductModel.filter(id__gte=begin, id__lte=end)


async def get_product_by_id_service(id: int) -> ProductModel:
    """Returns a single product by id. Raises 404 if not found."""
    return await get_product_by_id(id)


async def create_product_service(create_product_schema: CreateProductSchema) -> ProductModel:
    """Creates and returns a new product."""
    return await ProductModel.create(**create_product_schema.model_dump())


async def update_product_by_id_service(id: int, update_product_schema: UpdateProductSchema) -> ProductModel:
    """Updates and returns the product with the given id. Raises 404 if not found."""
    update_data = update_product_schema.model_dump(exclude_unset=True)
    product = await get_product_by_id(id)

    await product.update_from_dict(update_data)
    await product.save()

    return product


async def delete_product_by_id_service(id: int) -> None:
    """Deletes the product with the given id. Raises 404 if not found."""
    product = await get_product_by_id(id)
    await product.delete()