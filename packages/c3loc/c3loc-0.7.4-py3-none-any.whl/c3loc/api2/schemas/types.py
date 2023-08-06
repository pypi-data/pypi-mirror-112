from enum import IntEnum
from typing import Dict, Union

from pydantic import ConstrainedInt

Attributes = Dict[str, Union[str, int, bytes]]


class DbInteger(ConstrainedInt):
    min = 0
    max = 2**31 - 1


class Unsigned32Bit(ConstrainedInt):
    ge = 0
    lt = 2**32


class Unsigned16Bit(Unsigned32Bit):
    lt = 2**16


SensorValueType = Union[float, int]


class SensorType(IntEnum):
    SensorDataTemp = 0x01
    SensorDataHumid = 0x02
    SensorDataAuth = 0xff


__all__ = ['Attributes', 'DbInteger', 'Unsigned16Bit', 'Unsigned32Bit',
           'SensorType', 'SensorValueType']
