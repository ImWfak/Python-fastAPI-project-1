from enum import Enum


class ExceptionSourceEnum(str, Enum):
    PRODUCT_SERVICE = "PRODUCT_SERVICE"
    USER_SERVICE = "USER_SERVICE"
    AUTH_SERVICE = "AUTH_SERVICE"
