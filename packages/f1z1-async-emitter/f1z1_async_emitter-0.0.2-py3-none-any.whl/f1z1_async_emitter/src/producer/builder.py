# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common import CoroOrFunction, TimestampUnit, TimestampUtil, is_validators

from ..components import CountGenerator, Speed, EmitRecorder, EmitTaskQueue, SpeedTypes, SpeedUnit, Size
from .base import IBuilder
from .worker import EmitWorker


class EmitWorkerBuilder(IBuilder):
    """
    worker builder
    """

    def __init__(self,
                 target: CoroOrFunction,
                 speed: SpeedTypes,
                 count: Size = 1):

        self._target = target
        self._args = []
        self._kwargs = {}

        """ 辅助变量 """
        self._count: Size = count  # run count
        self._thread_workers: Size = None
        self._speed = speed  # speed
        self._unit: SpeedUnit = TimestampUnit.MILLISECOND  # speed unit

    @property
    def target(self):
        return self._target

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count: Size):
        self._check_int(count)
        self._count = count

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed: SpeedTypes):
        TimestampUtil.check_timestamp(speed)
        self._speed = speed

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit: TimestampUnit):
        TimestampUtil.check_timestamp_unit(unit)
        self._unit = unit

    @property
    def thread_workers(self):
        return self._thread_workers

    @thread_workers.setter
    def thread_workers(self, workers: Size):
        self._check_int(workers)
        self._thread_workers = workers

    def add_args(self, value):
        self._args.append(value)

    def set_kwargs(self, key, value):
        self._kwargs[key] = value

    def build(self) -> EmitWorker:
        speed = Speed(self.speed, self.unit)
        count = self.count
        return EmitWorker(
            self.target,
            counter=CountGenerator(speed, count),
            tasks=EmitTaskQueue(count),
            recorder=EmitRecorder(),
            args=self.to_args(),
            kwargs=self.to_kwargs(),
            thread_workers=self.thread_workers
        )

    def to_args(self):
        return tuple(self._args)

    def to_kwargs(self):
        if not self._kwargs:
            return {}
        return {k: v for k, v in self._kwargs.items()}

    def _check_int(self, value):
        if not is_validators.is_int(value):
            raise ValueError(
                f"value need int, but got {type(value).__name__}"
            )
