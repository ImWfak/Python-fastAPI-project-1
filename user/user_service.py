from http import HTTPStatus

from auth.auth_service import hash_password
from exception.app_exception import AppException
from exception.exeption_source_enum import ExceptionSourceEnum
from user.user_model import UserModel
from user.user_schema import CreateUserSchema, UpdateUserSchema


def _not_found(detail: str) -> AppException:
    return AppException(
        message=detail,
        exception_source=ExceptionSourceEnum.USER_SERVICE,
        http_status_code=HTTPStatus.NOT_FOUND,
    )


def _conflict(detail: str) -> AppException:
    return AppException(
        message=detail,
        exception_source=ExceptionSourceEnum.USER_SERVICE,
        http_status_code=HTTPStatus.CONFLICT,
    )


async def get_user_by_id(id: int) -> UserModel:
    """Internal helper — raises 404 if the user does not exist."""
    if user := await UserModel.get_or_none(id=id):
        return user
    raise _not_found(f"User with id {id} not found")


async def get_user_by_username(username: str) -> UserModel:
    """Internal helper — raises 404 if the user does not exist."""
    if user := await UserModel.get_or_none(username=username):
        return user
    raise _not_found(f"User with username {username} not found")


async def get_all_users_service() -> list[UserModel]:
    """Returns all users."""
    return await UserModel.all()


async def get_some_users_service(begin: int, end: int) -> list[UserModel]:
    """Returns all users whose id falls in the inclusive range [begin, end]."""
    return await UserModel.filter(id__gte=begin, id__lte=end)


async def get_user_by_id_service(id: int) -> UserModel:
    """Returns a single user by id. Raises 404 if not found."""
    return await get_user_by_id(id)


async def get_user_by_username_service(username: str) -> UserModel:
    """Returns a single user by username. Raises 404 if not found."""
    return await get_user_by_username(username)


async def create_user_service(create_user_schema: CreateUserSchema) -> UserModel:
    """Creates and returns a new user. Raises 409 if the username is already taken."""
    if await UserModel.get_or_none(username=create_user_schema.username):
        raise _conflict(f"User with username {create_user_schema.username} already exists")

    return await UserModel.create(
        username=create_user_schema.username,
        password=await hash_password(create_user_schema.password),
        user_access=create_user_schema.user_access,
    )


async def update_user_by_id_service(id: int, update_user_schema: UpdateUserSchema) -> UserModel:
    """Updates and returns the user with the given id. Raises 404 if not found, 409 if the new username is taken."""
    update_data = update_user_schema.model_dump(exclude_unset=True)
    user = await get_user_by_id(id)

    if new_username := update_data.get("username"):
        existing = await UserModel.get_or_none(username=new_username)
        if existing and existing.id != user.id:
            raise _conflict(f"User with username {new_username} already exists")

    if password := update_data.get("password"):
        update_data["password"] = await hash_password(password)

    await user.update_from_dict(update_data)
    await user.save()

    return user


async def delete_user_by_id_service(id: int) -> None:
    """Deletes the user with the given id. Raises 404 if not found."""
    user = await get_user_by_id(id)
    await user.delete()
