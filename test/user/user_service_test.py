import pytest
from pydantic import ValidationError

from auth.auth_service import verify_password_service
from exception.app_exception import AppException
from test_config import TestUserStandardValues, TestValidationRegexes
from user.conftest import standard_user
from user.user_asserts import (
    assert_standard_user,
    assert_user_not_found_by_id,
    assert_user_not_found_by_username,
    assert_username_already_exists,
)
from user.user_model import UserModel
from user.user_schema import CreateUserSchema, UpdateUserSchema
from user.user_service import (
    get_all_users_service,
    get_some_users_service,
    get_user_by_id_service,
    get_user_by_username_service,
    create_user_service,
    update_user_by_id_service,
    delete_user_by_id_service,
)

pytestmark = pytest.mark.asyncio


async def test_1_get_all_users_service() -> None:
    """Returns an empty list when no users exist."""
    all_users = await get_all_users_service()
    assert len(all_users) == 0


async def test_2_get_all_users_service(standard_user: UserModel) -> None:
    """Returns a single user matching the standard fixtures after one is created."""
    all_users = await get_all_users_service()

    assert len(all_users) == 1
    await assert_standard_user(all_users[0])


async def test_1_get_some_users_service() -> None:
    """Returns an empty list when begin=0 and end=0."""
    some_users = await get_some_users_service(0, 0)
    assert len(some_users) == 0


async def test_2_get_some_users_service() -> None:
    """Returns an empty list when begin=0 (no valid lower bound)."""
    record_with_max_id = await UserModel.all().order_by("-id").first()
    max_id = record_with_max_id.id if record_with_max_id else 2_147_483_647

    some_users = await get_some_users_service(0, max_id)
    assert len(some_users) == 0


async def test_3_get_some_users_service(standard_user: UserModel) -> None:
    """Returns an empty list for range (0, 0) even after a user is created."""
    some_users = await get_some_users_service(0, 0)
    assert len(some_users) == 0


async def test_4_get_some_users_service(standard_user: UserModel) -> None:
    """Returns exactly the created user when its id is within the requested range."""
    some_users = await get_some_users_service(standard_user.id, standard_user.id + 1)

    assert len(some_users) == 1
    await assert_standard_user(some_users[0])


async def test_1_get_user_by_id_service() -> None:
    """Raises 404 AppException for a non-existent id."""
    with pytest.raises(AppException) as app_exception:
        await get_user_by_id_service(TestUserStandardValues.nonexistent_id)

    await assert_user_not_found_by_id(
        TestUserStandardValues.nonexistent_id,
        app_exception,
    )


async def test_2_get_user_by_id_service(standard_user: UserModel) -> None:
    """Returns a user matching the standard fixtures for an existing id."""
    found_user = await get_user_by_id_service(standard_user.id)
    await assert_standard_user(found_user)


async def test_1_get_user_by_username_service() -> None:
    """Raises 404 AppException for a non-existent username."""
    with pytest.raises(AppException) as app_exception:
        await get_user_by_username_service(TestUserStandardValues.nonexistent_username)

    await assert_user_not_found_by_username(
        TestUserStandardValues.nonexistent_username,
        app_exception,
    )


async def test_2_get_user_by_username_service(standard_user: UserModel) -> None:
    """Returns a user matching the standard fixtures for an existing username."""
    found_user = await get_user_by_username_service(standard_user.username)

    await assert_standard_user(found_user)


async def test_1_create_user_service() -> None:
    """Creates and returns a user matching the standard fixtures."""
    created_user = await create_user_service(CreateUserSchema(
        username=TestUserStandardValues.username,
        password=TestUserStandardValues.password,
        user_access=TestUserStandardValues.user_access,
    ))

    await assert_standard_user(created_user)


async def test_2_create_user_service() -> None:
    """Raises a string_type ValidationError when username is not a string."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for CreateUserSchema\nusername\n\\s+{TestValidationRegexes.string_type_pattern}$",
    ):
        CreateUserSchema(
            username=TestUserStandardValues.wrong_type_username,
            password=TestUserStandardValues.password,
            user_access=TestUserStandardValues.user_access,
        )


async def test_3_create_user_service() -> None:
    """Raises a string_type ValidationError when password is not a string."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for CreateUserSchema\npassword\n\\s+{TestValidationRegexes.string_type_pattern}$",
    ):
        CreateUserSchema(
            username=TestUserStandardValues.username,
            password=TestUserStandardValues.wrong_type_password,
            user_access=TestUserStandardValues.user_access,
        )


async def test_4_create_user_service() -> None:
    """Raises an enum ValidationError when user_access is invalid."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for CreateUserSchema\nuser_access\n\\s+{TestValidationRegexes.enum_type_pattern}$",
    ):
        CreateUserSchema(
            username=TestUserStandardValues.username,
            password=TestUserStandardValues.password,
            user_access=TestUserStandardValues.wrong_type_user_access,
        )


async def test_5_create_user_service(standard_user: UserModel) -> None:
    """Raises 409 AppException when the username is already taken."""
    with pytest.raises(AppException) as app_exception:
        await create_user_service(CreateUserSchema(
            username=standard_user.username,
            password=standard_user.password,
            user_access=standard_user.user_access,
        ))

    await assert_username_already_exists(TestUserStandardValues.username, app_exception)


async def test_1_update_user_service() -> None:
    """Raises 404 AppException when attempting to update a non-existent user."""
    with pytest.raises(AppException) as app_exception:
        await update_user_by_id_service(
            TestUserStandardValues.nonexistent_id, UpdateUserSchema(
                username=TestUserStandardValues.updated_username,
                password=TestUserStandardValues.updated_password,
                user_access=TestUserStandardValues.updated_user_access,
        ))

    await assert_user_not_found_by_id(
        TestUserStandardValues.nonexistent_id,
        app_exception,
    )


async def test_2_update_user_service() -> None:
    """Raises a string_type ValidationError when username is not a string."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for UpdateUserSchema\nusername\n\\s+{TestValidationRegexes.string_type_pattern}$",
    ):
        UpdateUserSchema(
            username=TestUserStandardValues.wrong_type_username,
            password=TestUserStandardValues.password,
            user_access=TestUserStandardValues.user_access,
        )


async def test_3_update_user_service() -> None:
    """Raises a string_type ValidationError when password is not a string."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for UpdateUserSchema\npassword\n\\s+{TestValidationRegexes.string_type_pattern}$",
    ):
        UpdateUserSchema(
            username=TestUserStandardValues.updated_username,
            password=TestUserStandardValues.wrong_type_password,
            user_access=TestUserStandardValues.updated_user_access,
        )


async def test_4_update_user_service() -> None:
    """Raises an enum ValidationError when user_access is invalid."""
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for UpdateUserSchema\nuser_access\n\\s+{TestValidationRegexes.enum_type_pattern}$",
    ):
        UpdateUserSchema(
            username=TestUserStandardValues.updated_username,
            password=TestUserStandardValues.updated_password,
            user_access=TestUserStandardValues.wrong_type_user_access,
        )


async def test_5_update_user_service(standard_user: UserModel) -> None:
    """Correctly persists updated fields for an existing user."""
    updated_user = await update_user_by_id_service(
        standard_user.id,
        UpdateUserSchema(
            username=TestUserStandardValues.updated_username,
            password=TestUserStandardValues.updated_password,
            user_access=TestUserStandardValues.updated_user_access,
        ),
    )

    assert updated_user.username == TestUserStandardValues.updated_username
    assert await verify_password_service(TestUserStandardValues.updated_password, updated_user.password)
    assert updated_user.user_access == TestUserStandardValues.updated_user_access


async def test_1_delete_user_service() -> None:
    """Raises 404 AppException when attempting to delete a non-existent user."""
    with pytest.raises(AppException) as app_exception:
        await delete_user_by_id_service(TestUserStandardValues.nonexistent_id)

    await assert_user_not_found_by_id(
        TestUserStandardValues.nonexistent_id,
        app_exception,
    )


async def test_2_delete_user_service(standard_user: UserModel) -> None:
    """Deletes the user and confirms it is no longer retrievable."""
    id = standard_user.id

    await delete_user_by_id_service(id)

    assert await UserModel.get_or_none(id=id) is None