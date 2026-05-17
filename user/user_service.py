from http import HTTPStatus

from exception.exeption_source_enum import ExceptionSourceEnum
from exception.app_exception import AppException
from user.user_model import UserModel
from user.user_schema import (
    CreateUserSchema,
    UpdateUserSchema
)


async def get_user_by_id(id: int) -> UserModel:
    found_user: UserModel | None = await UserModel.get_or_none(id=id)

    if not found_user:
        raise AppException(
            message=f"User with id {id} not found",
            exception_source=ExceptionSourceEnum.USER_SERVICE,
            http_status_code=HTTPStatus.NOT_FOUND
        )

    return found_user


async def get_user_by_username(username: str) -> UserModel:
    found_user: UserModel | None = await UserModel.get_or_none(username=username)

    if not found_user:
        raise AppException(
            message=f"User with username {username} not found",
            exception_source=ExceptionSourceEnum.USER_SERVICE,
            http_status_code=HTTPStatus.NOT_FOUND
        )

    return found_user


async def get_all_users_service() -> list[UserModel]:
    return await UserModel.all()


async def get_some_users_service(begin: int, end: int) -> list[UserModel]:
    return await UserModel.filter(id_gte=begin, id_lte=end)


async def get_user_by_id_service(id: int) -> UserModel:
    return await get_user_by_id(id)


async def get_user_by_username_service(username: str) -> UserModel:
    return await get_user_by_username(username)


async def create_user_service(create_user_schema: CreateUserSchema) -> UserModel:
    return await UserModel.create(**create_user_schema.model_dump())


async def update_user_by_id_service(id: int, update_user_schema: UpdateUserSchema) -> UserModel:
    update_data: dict = update_user_schema.model_dump(exclude_unset=True)

    user_for_update: UserModel = await get_user_by_id(id)

    new_username: str | None = update_data.get("username")

    if new_username is not None:
        user_for_check: UserModel | None = await UserModel.get_or_none(username=new_username)

        if user_for_check and user_for_update.id != user_for_check.id:
            raise AppException(
                message=f"User with username {new_username} already exists",
                exception_source=ExceptionSourceEnum.USER_SERVICE,
                http_status_code=HTTPStatus.CONFLICT
            )

    await user_for_update.update_from_dict(update_data)
    await user_for_update.save()

    return user_for_update


async def delete_user_by_id_service(id: int) -> None:
    user_for_delete: UserModel = await get_user_by_id(id)

    await user_for_delete.delete()
