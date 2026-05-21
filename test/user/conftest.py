import pytest_asyncio

from auth.auth_service import hash_password_service
from user.user_model import UserModel
from user_constants import (
    STANDARD_USERNAME,
    STANDARD_PASSWORD,
    STANDARD_USER_ACCESS
)


@pytest_asyncio.fixture
async def standard_user() -> UserModel:
    hashed_standard_password = await hash_password_service(STANDARD_PASSWORD)

    return await UserModel.create(
        username=STANDARD_USERNAME,
        password=hashed_standard_password,
        user_access=STANDARD_USER_ACCESS
    )
