"""Constants."""

from enum import IntEnum, StrEnum


class Limits(IntEnum):
    GEM_NAME_MAX_CHAR = 50
    TOP_CUSTOMER_VALUE_LIMIT = 5
    MIN_GEMS_VALUE_LIMIT = 2


class Regex(StrEnum):
    GEM_NAME_REGEX = r"[а-яА-ЯёЁ -]+$"
