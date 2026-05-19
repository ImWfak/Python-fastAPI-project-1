import pytest_asyncio

from user.user_model import UserModel
from user_constants import (
    STANDARD_USERNAME,
    STANDARD_PASSWORD,
    STANDARD_USER_ACCESS
)


@pytest_asyncio.fixture
async def standard_user() -> UserModel:
    return await UserModel.create(
        username=STANDARD_USERNAME,
        password=STANDARD_PASSWORD,
        user_access=STANDARD_USER_ACCESS
    )
