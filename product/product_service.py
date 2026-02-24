from product.product_schemas import *
from product.product_model import ProductModel


async def get_product_by_id_or_raise_service(id: int) -> ProductModel:
    founded_product: ProductModel | None = await ProductModel.get_or_none(id=id)

    if not founded_product:
        raise Exception(f"Product with id {id} not found")

    return founded_product


async def get_all_products_service() -> list[ProductModel]:
    return await ProductModel.all()


async def get_some_products_service(begin: int, end: int) -> list[ProductModel]:
    return await ProductModel.filter(id__gte=begin, id__lte=end)


async def get_product_by_id_service(id: int) -> ProductModel:
    return await get_product_by_id_or_raise_service(id)


async def create_product_service(create_product_schema: CreateProductSchema) -> ProductModel:
    return await ProductModel(**create_product_schema.model_dump())


async def update_product_service(id: int, update_product_schema: UpdateProductSchema) -> ProductModel:
    update_data = update_product_schema.model_dump(exclude_unset=True)

    product_for_update: ProductModel = await get_product_by_id_or_raise_service(id)

    await product_for_update.save(**update_data)
    return await ProductModel.get(id=id)


async def delete_product_service(id: int) -> None:
    product_for_delete: ProductModel = await get_product_by_id_or_raise_service(id)

    await product_for_delete.delete()
