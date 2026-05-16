from tortoise import models, fields

from db.timestamp_mixin import TimestampMixin
from user.user_access_enum import UserAccessEnum


class ProductModel(
    models.Model,
    TimestampMixin
):
    id = fields.IntField(primary_key=True)

    name = fields.CharField(
        rquired=True,
        max_length=255
    )

    price_in_cents = fields.DecimalField(
        required=True,
        decimal_places=0,
        max_digits=10,
        min_value=1
    )

    user_access = fields.CharEnumField(
        enum_type=UserAccessEnum,
        max_lenght=6,
        required=True
    )

    class Meta:
        table = "products"
