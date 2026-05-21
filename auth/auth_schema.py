import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from pydantic import BaseModel

from user.user_access_enum import UserAccessEnum
from user.user_model import UserModel

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

class SingInSchema(BaseModel):
    username: str
    password: str


class SignUpSchema(SingInSchema):
    user_access: UserAccessEnum


class TokenPayloadSchema(BaseModel):
    username: str
    user_access: UserAccessEnum
    exp: datetime

    @classmethod
    async def from_user_model(cls, user_model: UserModel):
        return cls(
            username=user_model.username,
            user_access=user_model.user_access,
            exp=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
