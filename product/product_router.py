from fastapi import APIRouter

from product.product_model import ProductModel
from product.product_schemas import (
    GetProductSchema,
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

product_router = APIRouter(
    prefix="/product",
    tags=["product"]
)


@product_router.get("/", response_model=list[GetProductSchema])
async def get_all_products_router() -> list[ProductModel]:
    return await get_all_products_service()


@product_router.get("/some", response_model=list[GetProductSchema])
async def get_some_products_router(begin: int, end: int) -> list[ProductModel]:
    return await get_some_products_service(begin, end)


@product_router.get("/{id}", response_model=GetProductSchema)
async def get_product_by_id_router(id: int) -> ProductModel:
    return await get_product_by_id_service(id)


@product_router.post("/", response_model=GetProductSchema)
async def create_product_router(create_product_schema: CreateProductSchema) -> ProductModel:
    return await create_product_service(create_product_schema)


@product_router.patch("/{id}", response_model=GetProductSchema)
async def update_product_router(id: int, update_product_schema: UpdateProductSchema) -> ProductModel:
    return await update_product_service(id, update_product_schema)


@product_router.delete("/{id}", status_code=204)
async def delete_product_router(id: int) -> None:
    await delete_product_service(id)
