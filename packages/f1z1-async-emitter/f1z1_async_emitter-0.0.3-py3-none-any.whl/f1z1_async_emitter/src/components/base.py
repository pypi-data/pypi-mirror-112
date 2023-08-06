# @Time     : 2021/6/2
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import Task
from typing import Iterable, List, TypeVar, Union

T = TypeVar("T")
IterOrList = Union[
    Iterable[T],
    List[T]
]
Size = Union[int, None]


class IAwaitSpeed(object):
    """
    speed interface
    """

    def __await__(self):
        raise NotImplementedError("NotImplemented .__await__()")


class IAsyncCountGenerator(object):
    """
    count generator interface
    """

    def __aiter__(self) -> Iterable[int]:
        raise NotImplementedError("NotImplemented .__aiter__() -> Iterable[int]")


class IEmitAWaitQueue(object):
    """
    wait emit queue
    This's a support __aiter__ of Product Queue
    It support set get speed
    """

    def put(self, iter_or_list: IterOrList) -> None:
        """
        put  iter_or_list
        :param iter_or_list:
        :return:
        """
        raise NotImplementedError("NotImplemented .put(emitter)")

    def pop(self) -> T:
        """
        get emitter
        :return:
        """
        raise NotImplementedError("NotImplemented .get() -> IEmitter")

    def empty(self) -> bool:
        """
        queue empty()
        :return:
        """
        raise NotImplementedError("NotImplemented .empty() -> bool")

    async def __aiter__(self) -> Iterable[T]:
        """
        async iter IEmitter
        :return:
        """
        raise NotImplementedError("NotImplemented .__iter__() -> Iterable[IEmitter]")


class IEmitTaskQueue(object):
    """
    task emit queue

    This's a support __iter__ of Costume Queue
    """

    def put(self, task: Task) -> None:
        raise NotImplementedError("NotImplemented .put(task) -> None")

    def pop(self) -> Task:
        raise NotImplementedError("NotImplemented .pop() -> Task")

    def __iter__(self) -> Iterable[Task]:
        raise NotImplementedError("NotImplemented __iter__() -> Iterable[Task]")


class IEmitRecorder(object):
    """
    recorder interface
    save result
    """

    def save(self, result: T) -> None:
        raise NotImplementedError("NotImplemented .save(result) -> None")

    def __iter__(self) -> Iterable[T]:
        raise NotImplementedError("NotImplemented .__iter__() -> Iterable[T]")


class IEmitTaskSet(object):
    """
    worker collection
    """

    def add(self, worker: T):
        raise NotImplementedError("NotImplemented .add(worker)")

    def __iter__(self) -> Iterable[T]:
        raise NotImplementedError("NotImplemented .__iter__()")
