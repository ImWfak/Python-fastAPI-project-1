from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AbstractProductSchema(BaseModel):
    name: str
    price_in_cents: Decimal

    model_config = ConfigDict(from_attributes=True)


class CreateProductSchema(AbstractProductSchema):
    pass


class GetProductSchema(AbstractProductSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class UpdateProductSchema(AbstractProductSchema):
    name: str | None
    price_in_cents: Decimal | None
