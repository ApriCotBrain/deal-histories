"""Constants."""

from enum import IntEnum, StrEnum


class Limits(IntEnum):
    GEM_NAME_MAX_CHAR = 50
    USER_SPENT_MONEY_VALUE = 0
    TOP_CUSTOMER_VALUE_LIMIT = 5
    MIN_GEMS_VALUE = 2
    DEAL_TOTAL_DEFAULT_VALUE = 0
    DEAL_QUANTITY_DEFAULT_VALUE = 1


class Regex(StrEnum):
    GEM_NAME = r"[а-яА-ЯёЁ -]+$"
