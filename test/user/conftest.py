import pytest_asyncio

from auth.password_service import hash_password_service
from test_config import UserStandardValues
from user.user_model import UserModel


@pytest_asyncio.fixture
async def standard_user() -> UserModel:
    hashed_standard_password = await hash_password_service(UserStandardValues.password)

    return await UserModel.create(
        username=UserStandardValues.username,
        password=hashed_standard_password,
        user_access=UserStandardValues.user_access,
    )
