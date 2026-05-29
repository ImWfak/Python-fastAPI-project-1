import pytest_asyncio

from product.product_model import ProductModel
from test_config import TestProductStandardValues


@pytest_asyncio.fixture
async def standard_product() -> ProductModel:
    """
    Creates and returns a product with standard test fixtures.

    :returns: The newly created :class:`ProductModel` instance.
    """
    return await ProductModel.create(
        name=TestProductStandardValues.name,
        price_in_cents=TestProductStandardValues.price_in_cents,
        user_access=TestProductStandardValues.user_access,
    )
