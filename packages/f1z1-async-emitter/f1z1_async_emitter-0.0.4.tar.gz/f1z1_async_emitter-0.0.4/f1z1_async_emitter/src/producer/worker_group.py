# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Iterable, List, Union

from f1z1_common import CoroOrFunction, TaskFactory

from ..components import IEmitAWaitQueue, IEmitTaskQueue, IEmitRecorder
from ..customer import WorkerJoin
from .base import IWorker, IWorkerGroup

Workers = Union[
    Iterable[IWorker],
    List[IWorker]
]


class EmitWorkerGroup(IWorkerGroup):

    def __init__(self, buffer: IEmitAWaitQueue, tasks: IEmitTaskQueue, recorder: IEmitRecorder):
        """

        :param buffer: buffer queue
        :param tasks:  task queue
        :param recorder: recorder
        """
        self._buffer = buffer
        self._tasks = tasks
        self._recorder = recorder

    @property
    def buffer(self):
        return self._buffer

    @property
    def tasks(self):
        return self._tasks

    @property
    def recorder(self):
        return self._recorder

    def stuff(self, workers: Workers) -> None:
        filtered = self._filter_workers(workers)
        self.buffer.put(filtered)

    async def start(self):
        async for worker in self.buffer:
            self._put_to_queue(worker)

        # 交由消费侧
        result = await self.join()
        return result

    async def join(self):
        _join = self._join(self.recorder, self.tasks)
        return await _join.join()

    def _join(self, recorder: IEmitRecorder, task: IEmitTaskQueue) -> WorkerJoin:
        return WorkerJoin(recorder, task)

    def _put_to_queue(self, worker: IWorker):
        """
        worker to queue
        :param worker:
        :return:
        """
        task = self._to_task(worker.start())
        self._add_task(task)

    def _add_task(self, task):
        self.tasks.put(task)

    def _to_task(self, coro_or_func: CoroOrFunction):
        return TaskFactory(coro_or_func).create_task()

    def _filter_workers(self, workers: Workers):
        """
        过滤 worker
        :param workers:
        :return:
        """
        return (worker for _, worker in enumerate(workers) if self._is_worker(worker))

    def _is_worker(self, value):
        return isinstance(value, IWorker)
