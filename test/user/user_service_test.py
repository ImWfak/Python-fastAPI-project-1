import pytest
from pydantic import ValidationError

from constants import (
    NONEXISTENT_ID,
    STRING_TYPE_PATTERN,
    ENUM_TYPE_PATTERN
)
from exception.app_exception import AppException
from user.conftest import standard_user
from user.user_access_enum import UserAccessEnum
from user.user_asserts import (
    assert_standard_user,
    assert_user_not_found_by_id,
    assert_user_not_found_by_username,
    assert_username_already_exists
)
from user.user_model import UserModel
from user.user_schema import (
    CreateUserSchema,
    UpdateUserSchema
)
from user.user_service import (
    get_all_users_service,
    get_some_users_service,
    get_user_by_id_service,
    get_user_by_username_service,
    create_user_service,
    update_user_by_id_service,
    delete_user_by_id_service
)
from user_constants import (
    NONEXISTENT_USERNAME,
    STANDARD_USERNAME,
    STANDARD_PASSWORD,
    STANDARD_USER_ACCESS,
    WRONG_USERNAME,
    WRONG_PASSWORD,
    WRONG_USER_ACCESS
)

pytestmark = pytest.mark.asyncio


async def test_1_get_all_users_service() -> None:
    all_users: list[UserModel] = await get_all_users_service()

    assert len(all_users) == 0


async def test_2_get_all_users_service(standard_user: UserModel) -> None:
    all_users: list[UserModel] = await get_all_users_service()

    assert len(all_users) == 1
    await assert_standard_user(all_users[0])


async def test_1_get_some_users_service() -> None:
    some_users: list[UserModel] = await get_some_users_service(0, 0)

    assert len(some_users) == 0


async def test_2_get_some_users_service() -> None:
    record_with_max_id = await UserModel.all().order_by("-id").first()
    max_id = record_with_max_id.id if record_with_max_id else 2_147_483_647

    some_users: list[UserModel] = await get_some_users_service(0, max_id)

    assert len(some_users) == 0


async def test_3_get_some_users_service(standard_user: UserModel) -> None:
    some_users: list[UserModel] = await get_some_users_service(0, 0)

    assert len(some_users) == 0


async def test_4_get_some_users_service(standard_user: UserModel) -> None:
    some_users: list[UserModel] = await get_some_users_service(
        standard_user.id,
        standard_user.id + 1
    )

    assert len(some_users) == 1
    await assert_standard_user(some_users[0])


async def test_1_get_user_by_id_service() -> None:
    with pytest.raises(AppException) as app_exception:
        await get_user_by_id_service(NONEXISTENT_ID)

    await assert_user_not_found_by_id(NONEXISTENT_ID, app_exception)


async def test_2_get_user_by_id_service(standard_user: UserModel) -> None:
    found_user: UserModel = await get_user_by_id_service(standard_user.id)

    await assert_standard_user(found_user)


async def test_1_get_user_by_username_service() -> None:
    with pytest.raises(AppException) as app_exception:
        await get_user_by_username_service(NONEXISTENT_USERNAME)

    await assert_user_not_found_by_username(NONEXISTENT_USERNAME, app_exception)


async def test_2_get_user_by_username_service(standard_user: UserModel) -> None:
    found_user: UserModel = await get_user_by_username_service(standard_user.username)

    await assert_standard_user(found_user)


async def test_1_create_user_srvice() -> None:
    create_user_schema = CreateUserSchema(
        username=STANDARD_USERNAME,
        password=STANDARD_PASSWORD,
        user_access=STANDARD_USER_ACCESS
    )

    created_user: UserModel = await create_user_service(create_user_schema)

    await assert_standard_user(created_user)


async def test_2_create_user_srvice() -> None:
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for CreateUserSchema\nusername\n\\s+{STRING_TYPE_PATTERN}$"
    ):
        CreateUserSchema(
            username=WRONG_USERNAME,
            password=STANDARD_PASSWORD,
            user_access=STANDARD_USER_ACCESS
        )


async def test_3_create_user_srvice() -> None:
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for CreateUserSchema\npassword\n\\s+{STRING_TYPE_PATTERN}$"
    ):
        CreateUserSchema(
            username=STANDARD_USERNAME,
            password=WRONG_PASSWORD,
            user_access=STANDARD_USER_ACCESS
        )


async def test_4_create_user_srvice() -> None:
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for CreateUserSchema\nuser_access\n\\s+{ENUM_TYPE_PATTERN}$"
    ):
        CreateUserSchema(
            username=STANDARD_USERNAME,
            password=STANDARD_PASSWORD,
            user_access=WRONG_USER_ACCESS
        )


async def test_5_create_user_srvice(standard_user: UserModel) -> None:
    with pytest.raises(AppException) as app_exception:
        create_user_schema = CreateUserSchema(
            username=standard_user.username,
            password=standard_user.password,
            user_access=standard_user.user_access
        )

        await create_user_service(create_user_schema)

    await assert_username_already_exists(STANDARD_USERNAME, app_exception)


async def test_1_update_user_srvice() -> None:
    update_user_schema = UpdateUserSchema(
        username=STANDARD_USERNAME,
        password=STANDARD_PASSWORD,
        user_access=STANDARD_USER_ACCESS
    )

    with pytest.raises(AppException) as app_exception:
        await update_user_by_id_service(NONEXISTENT_ID, update_user_schema)

    await assert_user_not_found_by_id(NONEXISTENT_ID, app_exception)


async def test_2_update_user_srvice() -> None:
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for UpdateUserSchema\nusername\n\\s+{STRING_TYPE_PATTERN}$"
    ):
        UpdateUserSchema(
            username=WRONG_USERNAME,
            password=STANDARD_PASSWORD,
            user_access=STANDARD_USER_ACCESS
        )


async def test_3_update_user_srvice() -> None:
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for UpdateUserSchema\npassword\n\\s+{STRING_TYPE_PATTERN}$"
    ):
        UpdateUserSchema(
            username=STANDARD_USERNAME,
            password=WRONG_PASSWORD,
            user_access=STANDARD_USER_ACCESS
        )


async def test_4_update_user_srvice() -> None:
    with pytest.raises(
            ValidationError,
            match=f"^1 validation error for UpdateUserSchema\nuser_access\n\\s+{ENUM_TYPE_PATTERN}$"
    ):
        UpdateUserSchema(
            username=STANDARD_USERNAME,
            password=STANDARD_PASSWORD,
            user_access=WRONG_USER_ACCESS
        )


async def test_5_update_user_srvice(standard_user: UserModel) -> None:
    updated_username = STANDARD_USERNAME + "_updated"
    updated_password = STANDARD_PASSWORD + "_updated"
    updated_user_access = UserAccessEnum.LOW

    update_user_schema = UpdateUserSchema(
        username=updated_username,
        password=updated_password,
        user_access=updated_user_access
    )

    updated_user: UserModel = await update_user_by_id_service(standard_user.id, update_user_schema)

    assert updated_user.username == updated_username
    assert updated_user.password == updated_password
    assert updated_user.user_access == updated_user_access


async def test_1_delete_user_srvice() -> None:
    with pytest.raises(AppException) as app_exception:
        await delete_user_by_id_service(NONEXISTENT_ID)

    await assert_user_not_found_by_id(NONEXISTENT_ID, app_exception)


async def test_2_delete_user_srvice(standard_user: UserModel) -> None:
    id: int = standard_user.id

    await delete_user_by_id_service(id)

    assert await UserModel.get_or_none(id=id) == None
