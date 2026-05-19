import pytest_asyncio

from product.product_model import ProductModel
from product_constants import (
    STANDARD_NAME,
    STANDARD_PRICE_IN_CENTS,
    STANDARD_USER_ACCESS
)


@pytest_asyncio.fixture
async def standard_product() -> ProductModel:
    """
    Creates and returns a product with standard test fixtures.

    :returns: The newly created :class:`ProductModel` instance.
    """
    return await ProductModel.create(
        name=STANDARD_NAME,
        price_in_cents=STANDARD_PRICE_IN_CENTS,
        user_access=STANDARD_USER_ACCESS
    )
