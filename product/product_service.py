from http import HTTPStatus

from exception.app_exception import AppException
from exception.exeption_source_enum import ExceptionSourceEnum
from product.product_model import ProductModel
from product.product_schema import (
    CreateProductSchema,
    UpdateProductSchema
)


async def get_product_by_id(id: int) -> ProductModel:
    """
    Fetches a product by its primary key, raising an exception if it does not exist.

    This is an internal helper used by other service functions to centralize the
    ``NOT_FOUND`` error path. Callers that need to look up a product before
    mutating or returning it should use this rather than querying the model directly,
    so that the error message and HTTP status code stay consistent across the service
    layer.

    :param id: Primary key of the product to look up.
    :returns: The matching :class:`~product.product_model.ProductModel` instance.
    :raises AppException: With ``HTTP 404 NOT_FOUND`` and source
        :attr:`~common.exeption_source_enum.ExceptionSourceEnum.PRODUCT_SERVICE`
        if no product with the given ``id`` exists.
    """
    found_product: ProductModel | None = await ProductModel.get_or_none(id=id)

    if not found_product:
        raise AppException(
            message=f"Product with id {id} not found",
            exception_source=ExceptionSourceEnum.PRODUCT_SERVICE,
            http_status_code=HTTPStatus.NOT_FOUND,
        )

    return found_product


async def get_all_products_service() -> list[ProductModel]:
    """
    Retrieves every product in the database.

    No filtering or ordering is applied; the returned list reflects the natural
    insertion order of the underlying table.

    :returns: A list of all :class:`~product.product_model.ProductModel` instances,
        or an empty list if the table contains no rows.
    """
    return await ProductModel.all()


async def get_some_products_service(begin: int, end: int) -> list[ProductModel]:
    """
    Retrieves all products whose primary key falls within the inclusive range
    ``[begin, end]``.

    Useful for paginating or batch-fetching records by ID when the caller already
    knows the ID boundaries of the desired window. Because IDs start at ``1``, passing
    ``begin=0`` always produces an empty list regardless of ``end``.

    :param begin: Lower bound of the ID range (inclusive).
    :param end: Upper bound of the ID range (inclusive).
    :returns: A list of :class:`~product.product_model.ProductModel` instances whose
        ``id`` satisfies ``begin <= id <= end``, or an empty list if no products fall
        within the range.
    """
    return await ProductModel.filter(id__gte=begin, id__lte=end)


async def get_product_by_id_service(id: int) -> ProductModel:
    """
    Retrieves a single product by its primary key.

    :param id: Primary key of the product to retrieve.
    :returns: The matching :class:`~product.product_model.ProductModel` instance.
    :raises AppException: With ``HTTP 404 NOT_FOUND`` if no product with the given
        ``id`` exists.
    """
    return await get_product_by_id(id)


async def create_product_service(create_product_schema: CreateProductSchema) -> ProductModel:
    """
    Persists a new product to the database.

    All fields from ``create_product_schema`` are forwarded directly to the ORM's
    ``create`` method. Validation is expected to have been performed by Pydantic
    before this function is called.

    :param create_product_schema: A validated schema containing the data for the new
        product.
    :returns: The newly created :class:`~product.product_model.ProductModel` instance,
        including its auto-assigned primary key.
    """
    return await ProductModel.create(**create_product_schema.model_dump())


async def update_product_by_id_service(id: int, update_product_schema: UpdateProductSchema) -> ProductModel:
    """
    Updates an existing product with the supplied field values and persists the changes.

    Only fields explicitly set on ``update_product_schema`` are applied; unset optional
    fields are ignored via ``exclude_unset=True``. The product is re-fetched before
    being returned so that the caller always receives the latest persisted state.

    :param id: Primary key of the product to update.
    :param update_product_schema: A validated schema containing the fields to update.
        Fields that were not explicitly supplied by the caller are excluded from the
        update.
    :returns: The updated :class:`~product.product_model.ProductModel` instance
        reflecting the new values.
    :raises AppException: With ``HTTP 404 NOT_FOUND`` if no product with the given
        ``id`` exists.
    """
    update_data: dict = update_product_schema.model_dump(exclude_unset=True)

    product_for_update: ProductModel = await get_product_by_id(id)

    await product_for_update.update_from_dict(update_data)
    await product_for_update.save()

    return product_for_update


async def delete_product_by_id_service(id: int) -> None:
    """
    Deletes an existing product from the database.

    The product is first fetched to confirm it exists before deletion. If it does not
    exist, an exception is raised before any destructive operation is attempted.

    :param id: Primary key of the product to delete.
    :returns: ``None`` on successful deletion.
    :raises AppException: With ``HTTP 404 NOT_FOUND`` if no product with the given
        ``id`` exists.
    """
    product_for_delete: ProductModel = await get_product_by_id(id)

    await product_for_delete.delete()