from tortoise import models, fields

from db.timestamp_mixin import TimestampMixin
from user.user_access_enum import UserAccessEnum


class UserModel(
    models.Model,
    TimestampMixin
):
    id = fields.IntField(primary_key=True)

    username = fields.CharField(
        max_length=255,
        unique=True
    )

    password = fields.CharField(
        required=True,
        max_length=255
    )

    user_access = fields.CharEnumField(
        enum_type=UserAccessEnum,
        max_length=6,
        required=True
    )

    class Meta:
        table = "users"
