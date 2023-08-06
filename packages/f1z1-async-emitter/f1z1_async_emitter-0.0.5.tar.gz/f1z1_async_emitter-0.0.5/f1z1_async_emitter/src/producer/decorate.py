# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Callable, Dict, Optional, Tuple
from functools import partial, wraps

from f1z1_common import CoroOrFunction, TimestampUnit

from ..components import CountGenerator, SpeedTypes, SpeedUnit, Size, Speed, EmitTaskQueue, EmitRecorder
from .worker import EmitWorker

DecorateReturn = Callable[[CoroOrFunction], Callable]
WrappedReturn = Callable[[Optional[Tuple], Optional[Dict]], EmitWorker]


def _factory(speed: SpeedTypes,
             count: Size = 1,
             unit: SpeedUnit = TimestampUnit.MILLISECOND,
             thread_workers: int = None):
    speed = Speed(speed, unit)
    return partial(
        EmitWorker,
        counter=CountGenerator(speed, count),
        tasks=EmitTaskQueue(count),
        thread_workers=thread_workers,
        recorder=EmitRecorder()
    )


def emit_decorate(speed: SpeedTypes,
                  count: Size = 1,
                  unit: SpeedUnit = TimestampUnit.MILLISECOND,
                  thread_workers: int = None) -> DecorateReturn:
    def decorator(func: CoroOrFunction) -> WrappedReturn:
        @wraps(func)
        def wrapped(*args, **kwargs) -> EmitWorker:
            f = _factory(speed, count, unit, thread_workers)
            return f(target=func, args=args, kwargs=kwargs)

        return wrapped

    return decorator
