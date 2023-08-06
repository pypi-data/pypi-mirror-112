# @Time     : 2021/6/3
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import abstractmethod
from enum import Enum
from typing import Union

from .enums import EnumUtil
from ..validator.is_validators import is_enum, is_number

TimestampTypes = Union[int, float]

BASE = 10


class TimestampUnit(Enum):
    SECOND = BASE ** 0
    MILLISECOND = BASE ** -3
    MICROSECOND = BASE ** -6


class ITimestamp:

    @classmethod
    @abstractmethod
    def to_timestamp(cls, int_or_float: TimestampTypes, time_unit: TimestampUnit) -> float:
        raise NotImplementedError()


def to_float(int_or_float: TimestampTypes) -> float:
    if not is_number(int_or_float):
        raise ValueError(
            f"int_or_float need int or float, but got {type(int_or_float).__name__}"
        )
    return float(int_or_float)


def to_unit(time_unit: TimestampUnit) -> TimestampTypes:
    if not is_enum(time_unit):
        raise ValueError(
            f"timestamp unit need Enum instance, but got {type(time_unit).__name__}"
        )

    return EnumUtil.unenum(time_unit)


class Second(ITimestamp):

    @classmethod
    def to_timestamp(cls, int_or_float: TimestampTypes, time_unit: TimestampUnit) -> TimestampTypes:
        return int_or_float * to_unit(time_unit)


class MicroSecond(ITimestamp):

    @classmethod
    def to_timestamp(cls, int_or_float: TimestampTypes, time_unit: TimestampUnit) -> TimestampTypes:
        return int_or_float * to_unit(time_unit)


class MilliSecond(ITimestamp):

    @classmethod
    def to_timestamp(cls, int_or_float: TimestampTypes, time_unit: TimestampUnit) -> TimestampTypes:
        return int_or_float * to_unit(time_unit)


class TimestampUtil(ITimestamp):

    @classmethod
    def to_timestamp(cls, timestamp: TimestampTypes, unit: TimestampUnit = TimestampUnit.MILLISECOND) -> float:
        f = {
            TimestampUnit.SECOND: Second.to_timestamp,
            TimestampUnit.MILLISECOND: MilliSecond.to_timestamp,
            TimestampUnit.MICROSECOND: MicroSecond.to_timestamp
        }.get(unit, MilliSecond.to_timestamp)
        return to_float(f(timestamp, unit))
