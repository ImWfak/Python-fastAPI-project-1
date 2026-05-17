from datetime import datetime

from pydantic import BaseModel, ConfigDict

from user_access_enum import UserAccessEnum


class AbstractUserSchema(BaseModel):
    username: str
    password: str
    user_access: UserAccessEnum

    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(AbstractUserSchema):
    pass


class GetUserSchema(AbstractUserSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class UpdateUserSchema(AbstractUserSchema):
    username: str | None
    password: str | None
    user_access: UserAccessEnum | None
