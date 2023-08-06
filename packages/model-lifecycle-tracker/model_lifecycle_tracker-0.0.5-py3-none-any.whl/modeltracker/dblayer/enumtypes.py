from enum import Enum, unique


@unique
class StateEnum(Enum):
    ACTIVE = 1
    INACTIVE = 2
    SUCCESS = 3
    FAIL = 4

