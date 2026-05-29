from abc import ABC
from dataclasses import dataclass
from decimal import Decimal

from pydantic.v1 import BaseSettings, Field

from user.user_access_enum import UserAccessEnum


class TestDBSettings(BaseSettings):
    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT")
    user: str = Field(alias="UESR")
    password: str = Field(alias="PASSWORD")
    database: str = Field(alias="DATABASE")

    class Config:
        env_file = ".test.env"


class TestTokenSettings(BaseSettings):
    secret_key: str = Field(alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_algorithm: str = Field(alias="JWT_ALGORITHM")

    class Config:
        env_file = ".test.env"


@dataclass(frozen=True)
class AbstractTestValues(ABC):
    nonexistent_id = -1


@dataclass(frozen=True)
class TestUserStandardValues(AbstractTestValues):
    nonexistent_username: str = ""

    username = "test username"
    password = "P@ssword"
    user_access = UserAccessEnum.MIDDLE

    updated_username = username + "_updated"
    updated_password = password + "_updated"
    updated_user_access = UserAccessEnum.LOW

    wrong_type_username = 0
    wrong_type_password = 0
    wrong_type_user_access = ""


@dataclass(frozen=True)
class TestProductStandardValues(AbstractTestValues):
    name = "test name"
    price_in_cents = Decimal(1)
    user_access = UserAccessEnum.MIDDLE

    updated_name = name + "_updated"
    updated_price_in_cents = price_in_cents + Decimal(1)
    updated_user_access = UserAccessEnum.LOW

    wrong_type_name = 0
    wrong_type_price_in_cents = ""
    wrong_type_user_access = ""


@dataclass(frozen=True)
class TestValidationRegexes:
    pydantic_base_url = r"https://errors\.pydantic\.dev/2\.12\/v"

    string_type_pattern = (
            r"Input should be a valid string "
            r"\[type=string_type, input_value=.+, input_type=int\]\n"
            r"\s+For further information visit " + pydantic_base_url + r"\/string_type"
    )
    decimal_type_pattern = (
            r"Input should be a valid decimal "
            r"\[type=decimal_parsing, input_value='', input_type=str\]\n"
            r"\s+For further information visit " + pydantic_base_url + r"\/decimal_parsing"
    )
    enum_type_pattern = (
            r"Input should be 'HIGH', 'MIDDLE' or 'LOW' "
            r"\[type=enum, input_value='', input_type=str]\n"
            r"\s+For further information visit " + pydantic_base_url + r"\/enum"
    )
