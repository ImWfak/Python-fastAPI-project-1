from decimal import Decimal

from user.user_access_enum import UserAccessEnum

STANDARD_NAME = "test name"
STANDARD_PRICE_IN_CENTS = Decimal("0")
STANDARD_USER_ACCESS = UserAccessEnum.MIDDLE

WRONG_NAME = 1
WRONG_PRICE_IN_CENTS = ""
WRONG_USER_ACCESS = ""
