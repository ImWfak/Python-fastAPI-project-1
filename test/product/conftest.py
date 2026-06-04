import pytest_asyncio

from product.product_model import ProductModel
from test_config import ProductStandardValues


@pytest_asyncio.fixture
async def standard_product() -> ProductModel:
    """
    Creates and returns a product with standard test fixtures.

    :returns: The newly created :class:`ProductModel` instance.
    """
    return await ProductModel.create(
        name=ProductStandardValues.name,
        price_in_cents=ProductStandardValues.price_in_cents,
        user_access=ProductStandardValues.user_access,
    )
