from datetime import datetime

from pydantic import BaseModel, ConfigDict

from user.user_access_enum import UserAccessEnum


class AbstractUserSchema(BaseModel):
    username: str
    user_access: UserAccessEnum

    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(AbstractUserSchema):
    password: str


class GetUserSchema(AbstractUserSchema):
    id: int
    password: bytes
    created_at: datetime
    updated_at: datetime


class UpdateUserSchema(AbstractUserSchema):
    username: str | None
    password: str | None
    user_access: UserAccessEnum | None
