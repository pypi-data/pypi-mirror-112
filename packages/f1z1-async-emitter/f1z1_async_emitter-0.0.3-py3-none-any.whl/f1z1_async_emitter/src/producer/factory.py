# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from multiprocessing import cpu_count

from f1z1_common import is_validators

from ..components import (
    EmitBufferQueue,
    EmitTaskQueue,
    EmitTaskSet,
    EmitRecorderChain,
    Speed,
    SpeedTypes,
    SpeedUnit,
    Size
)
from .base import IFactory
from .worker_group import EmitWorkerGroup
from .worker_master import EmitWorkerMaster


class EmitWorkerGroupFactory(IFactory):
    """
    worker group factory
    """

    @classmethod
    def create(cls,
               speed: SpeedTypes, *,
               speed_unit: SpeedUnit = None,
               maxsize: Size = None) -> EmitWorkerGroup:
        speed = Speed(speed, speed_unit)
        return EmitWorkerGroup(
            EmitBufferQueue(speed, maxsize),
            EmitTaskQueue(maxsize),
            EmitRecorderChain()
        )


class EmitWorkerMasterFactory(IFactory):
    """
    worker master factory
    """

    @classmethod
    def create(cls, maxsize: Size = None) -> EmitWorkerMaster:
        maxsize = cls._get_maxsize_with_cpu(maxsize)
        return EmitWorkerMaster(
            EmitTaskSet(maxsize),
            EmitRecorderChain()
        )

    @classmethod
    def _get_maxsize_with_cpu(cls, cpu: Size = None):
        min_cpu = cpu_count()
        if not is_validators.is_int(cpu):
            return min_cpu
        return min(abs(cpu), min_cpu)
