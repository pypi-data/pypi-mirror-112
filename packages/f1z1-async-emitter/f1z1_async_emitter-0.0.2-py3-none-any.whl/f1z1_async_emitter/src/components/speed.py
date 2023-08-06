# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import sleep
from collections.abc import Awaitable
from functools import lru_cache
from typing import Optional, Union

from f1z1_common import is_validators, TimestampUtil, TimestampUnit

from .base import IAwaitSpeed

SpeedTypes = Union[int, float]
SpeedUnit = Optional[TimestampUnit]


class Speed(Awaitable, IAwaitSpeed):
    """
    speed module
    """

    def __init__(self,
                 speed: SpeedTypes,
                 unit: SpeedUnit = TimestampUnit.MILLISECOND):
        self._speed = speed
        self._unit = unit

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed: SpeedTypes) -> None:
        self._check_speed(speed)
        self._speed = speed

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit: TimestampUnit) -> None:
        self._check_unit(unit)
        self._unit = unit

    def __await__(self):
        return self._await_speed(self.computed_speed_use_lru()).__await__()

    async def _await_speed(self, speed: SpeedTypes):
        return await sleep(speed)

    def computed_speed_use_lru(self):
        return self._get_speed_use_lru()

    @lru_cache()
    def _get_speed_use_lru(self):
        return TimestampUtil.to_timestamp(self.speed, self.unit)

    def _check_speed(self, speed):
        if not is_validators.is_number(speed):
            raise ValueError(f"speed need float or int, but got {type(speed).__name__}")

    def _check_unit(self, unit):
        if not is_validators.is_enum(unit):
            raise ValueError(f"unit need enum, but got {type(unit).__name__}")
