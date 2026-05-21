import os
from http import HTTPStatus

from dotenv import load_dotenv
from jose import jwt

from auth.auth_schema import TokenPayloadSchema, SignUpSchema, SingInSchema
from auth.password_service import verify_password_service
from exception.app_exception import AppException
from exception.exeption_source_enum import ExceptionSourceEnum
from user.user_model import UserModel
from user.user_schema import CreateUserSchema
from user.user_service import create_user_service, get_user_by_username_service

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]


async def create_access_token_service(token_payload_schema: TokenPayloadSchema) -> str:
    return jwt.encode(
        claims=token_payload_schema.model_dump(),
        key=SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


async def sign_in_service(sign_in_schema: SingInSchema) -> str:
    found_user: UserModel = await get_user_by_username_service(sign_in_schema.username)

    if not await verify_password_service(
            plain_password=sign_in_schema.password,
            hashed_password=found_user.password,
    ):
        raise AppException(
            message="Incorrect username or password",
            exception_source=ExceptionSourceEnum.AUTH_SERVICE,
            http_status_code=HTTPStatus.UNAUTHORIZED,
        )

    return await create_access_token_service(
        await TokenPayloadSchema.from_user_model(found_user)
    )


async def sign_up_service(sing_up_schema: SignUpSchema) -> str:
    created_user: UserModel = await create_user_service(
        await CreateUserSchema.from_sign_up_schema(sing_up_schema)
    )

    return await create_access_token_service(
        await TokenPayloadSchema.from_user_model(created_user)
    )
