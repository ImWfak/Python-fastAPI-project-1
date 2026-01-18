from tortoise import models, fields

from common.timestamp_mixin import TimestampMixin


class ProductModel(
    models.Model,
    TimestampMixin
):
    id = fields.IntField(pk=True)

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

    class Meta:
        table = "products"

