import bcrypt
import pytest

from auth.conftest import standard_hashed_password
from auth.password_service import verify_password_service
from test_config import UserStandardValues

pytestmark = pytest.mark.asyncio


async def test_1_hash_password_service(standard_hashed_password: bytes) -> None:
    assert bcrypt.checkpw(UserStandardValues.password.encode("utf-8"), standard_hashed_password)


async def test_2_hash_password_service(standard_hashed_password: bytes) -> None:
    assert not bcrypt.checkpw(UserStandardValues.updated_password.encode("utf-8"), standard_hashed_password)


async def test_1_verify_password_service(standard_hashed_password: bytes) -> None:
    assert await verify_password_service(UserStandardValues.password, standard_hashed_password)


async def test_2_verify_password_service(standard_hashed_password: bytes) -> None:
    assert not await verify_password_service(UserStandardValues.updated_password, standard_hashed_password)
