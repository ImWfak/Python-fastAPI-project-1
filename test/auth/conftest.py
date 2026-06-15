import bcrypt
import pytest_asyncio

from test_config import UserStandardValues


@pytest_asyncio.fixture()
async def standard_hashed_password() -> bytes:
    return bcrypt.hashpw(UserStandardValues.password.encode("utf-8"), bcrypt.gensalt())
