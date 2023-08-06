# @Time     : 2021/6/3
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import Task
from collections import deque
from typing import Deque

from f1z1_common import is_validators

from .base import IAwaitSpeed, IEmitAWaitQueue, IEmitTaskQueue, IEmitTaskSet, IterOrList, Size


class EmitBufferQueue(IEmitAWaitQueue):
    """
    emit buffer queue
    """

    def __init__(self, speed: IAwaitSpeed, maxsize: Size = None):
        self._speed = speed
        self._queue = deque(maxlen=maxsize)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed: IAwaitSpeed):
        self._check_speed(speed)
        self._speed = speed

    @property
    def length(self):
        return len(self._queue)

    def empty(self):
        return not self.length

    def put(self, iter_or_list: IterOrList):
        self._queue.extend(self._filter(iter_or_list))

    def pop(self):
        return self._queue.popleft()

    async def __aiter__(self):
        while True:
            if self.empty():
                break
            yield self.pop()
            await self.speed

    def _filter(self, iter_or_list: IterOrList) -> IterOrList:
        if not is_validators.is_iterable(iter_or_list):
            return []
        return iter_or_list

    def _check_speed(self, speed: IAwaitSpeed):
        if not isinstance(speed, IAwaitSpeed):
            raise ValueError(
                f"speed need IAwaitSpeed, but got {type(speed).__name__}"
            )


class EmitTaskQueue(IEmitTaskQueue):

    def __init__(self, maxsize: Size = None):
        self._queue: Deque[Task] = deque(maxlen=maxsize)

    @property
    def length(self):
        return len(self._queue)

    def empty(self):
        return not self.length

    def put(self, task: Task) -> None:
        self._check_task(task)
        self._queue.append(task)

    def pop(self):
        return self._queue.popleft()

    def __iter__(self):
        while True:
            if self.empty():
                break
            yield self.pop()

    def _check_task(self, value):
        if not isinstance(value, Task):
            raise ValueError(
                f"value need Task, but got {type(value).__name__}"
            )


class EmitTaskSet(IEmitTaskSet):
    """
    Emit Task Collection
    """

    def __init__(self, maxsize: Size = None):
        self._set = set()
        self._maxsize = maxsize

    @property
    def length(self):
        return len(self._set)

    def empty(self):
        return not self.length

    def full(self):
        maxsize = self._maxsize
        if maxsize is None:
            return False
        return self.length >= maxsize

    def add(self, worker):
        if self.full():
            return
        self._set.add(worker)

    def __iter__(self):
        if not self.empty():
            for _, worker in enumerate(self._set):
                yield worker

    def __str__(self):
        return str(self._set)