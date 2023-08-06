from enum import Enum
from typing import Dict, List, Union


Message = Dict[str, Union[str, Dict[str, int], List[Dict[str, str]]]]


class BlindsType(Enum):
    ROLLER_BLINDS = 0
    VENETIAN_BLINDS = 1
    ROMAN_BLINDS = 2
    HONEYCOMB_BLINDS = 3
    SHANGRI_LA_BLINDS = 4
    ROLLER_SHUTTER = 5
    ROLLER_GATE = 6
    AWNING = 7
    TDBU = 8
    DAY_AND_NIGHT_BLINDS = 9
    DIMMING_BLINDS = 10
    CURTAIN = 11
    CURTAIN_LEFT = 12
    CURTAIN_RIGHT = 13


class Operation(Enum):
    CLOSING = 0
    OPENING = 1
    STOPPED = 2
    STATUS_QUERY = 5


class LimitState(Enum):
    NOT_LIMITED = 0
    TOP_LIMIT_DETECTED = 1
    BOTTOM_LIMIT_DETECTED = 2
    BOTH_LIMITS_DETECTED = 3
    THIRD_LIMIT_DETECTED = 4


class VoltageMode(Enum):
    AC_MOTOR = 0
    DC_MOTOR = 1


class WirelessMode(Enum):
    UNIDIRECTIONAL = 0
    BIDIRECTIONAL = 1
    BIDIRECTIONAL_MECHANICAL_LIMITS = 2
    OTHER = 3
