from fastapi import APIRouter

from product.product_model import ProductModel
from product.product_schema import (
    CreateProductSchema,
    GetProductSchema,
    UpdateProductSchema,
)
from product.product_service import (
    create_product_service,
    delete_product_service,
    get_all_products_service,
    get_product_by_id_service,
    get_some_products_service,
    update_product_service,
)

product_router = APIRouter(
    prefix="/product",
    tags=["product"],
)


@product_router.get("/", response_model=list[GetProductSchema])
async def get_all_products_router() -> list[ProductModel]:
    """
    Retrieve all products.

    Returns every product in the database with no filtering or ordering applied.

    **Endpoint:** ``GET /product/``

    :returns: A list of all products serialized as :class:`~product.product_schema.GetProductSchema`,
        or an empty list if no products exist.
    """
    return await get_all_products_service()


@product_router.get("/some", response_model=list[GetProductSchema])
async def get_some_products_router(begin: int, end: int) -> list[ProductModel]:
    """
    Retrieve a range of products by ID.

    Returns all products whose primary key falls within the inclusive range
    ``[begin, end]``. Because product IDs start at ``1``, passing ``begin=0``
    always yields an empty list regardless of ``end``.

    **Endpoint:** ``GET /product/some?begin={begin}&end={end}``

    :param begin: Lower bound of the ID range (inclusive). Passed as a query parameter.
    :param end: Upper bound of the ID range (inclusive). Passed as a query parameter.
    :returns: A list of matching products serialized as
        :class:`~product.product_schema.GetProductSchema`, or an empty list if no
        products fall within the range.
    """
    return await get_some_products_service(begin, end)


@product_router.get("/{id}", response_model=GetProductSchema)
async def get_product_by_id_router(id: int) -> ProductModel:
    """
    Retrieve a single product by its primary key.

    **Endpoint:** ``GET /product/{id}``

    :param id: Primary key of the product to retrieve. Passed as a path parameter.
    :returns: The matching product serialized as
        :class:`~product.product_schema.GetProductSchema`.
    :raises AppException: With ``HTTP 404 NOT_FOUND`` if no product with the given
        ``id`` exists.
    """
    return await get_product_by_id_service(id)


@product_router.post("/", response_model=GetProductSchema)
async def create_product_router(create_product_schema: CreateProductSchema) -> ProductModel:
    """
    Create a new product.

    Accepts a JSON request body validated against
    :class:`~product.product_schema.CreateProductSchema` and persists the new product
    to the database.

    **Endpoint:** ``POST /product/``

    :param create_product_schema: Request body containing the data for the new product.
        FastAPI validates and deserializes it automatically.
    :returns: The newly created product, including its auto-assigned primary key,
        serialized as :class:`~product.product_schema.GetProductSchema`.
    :raises HTTPException: With ``HTTP 422 UNPROCESSABLE_CONTENT`` if the request body
        fails schema validation (e.g. ``name`` is not a string, or ``price_in_cents``
        is not a valid decimal).
    """
    return await create_product_service(create_product_schema)


@product_router.patch("/{id}", response_model=GetProductSchema)
async def update_product_router(id: int, update_product_schema: UpdateProductSchema) -> ProductModel:
    """
    Partially update an existing product.

    Accepts a JSON request body validated against
    :class:`~product.product_schema.UpdateProductSchema`. Only fields explicitly
    present in the request body are updated; omitted fields retain their current values.

    **Endpoint:** ``PATCH /product/{id}``

    :param id: Primary key of the product to update. Passed as a path parameter.
    :param update_product_schema: Request body containing the fields to update.
        FastAPI validates and deserializes it automatically.
    :returns: The updated product reflecting the new values, serialized as
        :class:`~product.product_schema.GetProductSchema`.
    :raises AppException: With ``HTTP 404 NOT_FOUND`` if no product with the given
        ``id`` exists.
    :raises HTTPException: With ``HTTP 422 UNPROCESSABLE_CONTENT`` if the request body
        fails schema validation (e.g. ``name`` is not a string, or ``price_in_cents``
        is not a valid decimal).
    """
    return await update_product_service(id, update_product_schema)


@product_router.delete("/{id}", status_code=204)
async def delete_product_router(id: int) -> None:
    """
    Delete an existing product.

    Permanently removes the product with the given ``id`` from the database. The
    product is confirmed to exist before any destructive operation is attempted.

    **Endpoint:** ``DELETE /product/{id}``

    :param id: Primary key of the product to delete. Passed as a path parameter.
    :returns: No content (``HTTP 204 NO_CONTENT``) on successful deletion.
    :raises AppException: With ``HTTP 404 NOT_FOUND`` if no product with the given
        ``id`` exists.
    """
    await delete_product_service(id)