import pytest_asyncio

from auth.password_service import hash_password_service
from test_config import TestUserStandardValues
from user.user_model import UserModel


@pytest_asyncio.fixture
async def standard_user() -> UserModel:
    hashed_standard_password = await hash_password_service(TestUserStandardValues.password)

    return await UserModel.create(
        username=TestUserStandardValues.username,
        password=hashed_standard_password,
        user_access=TestUserStandardValues.user_access,
    )
