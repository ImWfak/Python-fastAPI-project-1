from datetime import datetime

from pydantic import BaseModel, ConfigDict

from auth.auth_schema import SignUpSchema
from user.user_access_enum import UserAccessEnum


class AbstractUserSchema(BaseModel):
    username: str
    user_access: UserAccessEnum

    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(AbstractUserSchema):
    password: str

    @classmethod
    async def from_sign_up_schema(cls, sign_up_schema: SignUpSchema) -> CreateUserSchema:
        return cls(
            username=sign_up_schema.username,
            password=sign_up_schema.password,
            user_access=sign_up_schema.user_access
        )


class GetUserSchema(AbstractUserSchema):
    id: int
    password: bytes
    created_at: datetime
    updated_at: datetime


class UpdateUserSchema(AbstractUserSchema):
    username: str | None
    password: str | None
    user_access: UserAccessEnum | None
