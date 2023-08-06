# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import TypeVar

"""
生产侧接口
"""

T = TypeVar("T")


class IWorker(object):
    """
    worker interface
    """

    async def start(self) -> T:
        raise NotImplementedError("NotImplemented .start() -> T")


class IWorkerGroup(object):
    """
    worker group interface
    """

    def stuff(self, workers: T) -> None:
        """
        stuff workers
        :param workers:
        :return:
        """
        raise NotImplementedError("NotImplemented .stuff(workers) -> None")

    async def start(self) -> T:
        raise NotImplementedError("NotImplemented .start() -> T")


class IWorkerMaster(object):
    """
    worker master interface
    """

    def add(self, worker_or_group: T):
        raise NotImplementedError("NotImplemented .add(worker_or_group)")

    def start(self) -> T:
        raise NotImplementedError("NotImplemented .start() -> T")


class IBuilder(object):

    def build(self) -> T:
        raise NotImplementedError("NotImplemented .build() -> T")


class IFactory(object):

    @classmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError("NotImplemented .create() -> T")
