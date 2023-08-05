from enum import Enum


class Precision(Enum):
    EMPTY = 0
    YEAR = 4
    MONTH = 7
    DAY = 10
    HOUR = 13
    MINUTE = 16
    SECOND = 19
    FULL = SECOND
