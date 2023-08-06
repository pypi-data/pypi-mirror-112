# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common import ArgsTypes, CoroOrFunction, KwargsTypes, TaskFactory

from ..components import IAsyncCountGenerator, IEmitTaskQueue, IEmitRecorder
from ..customer import WorkerJoin
from .base import IWorker


class EmitWorker(IWorker):

    def __init__(self,
                 target: CoroOrFunction, *,
                 counter: IAsyncCountGenerator,
                 tasks: IEmitTaskQueue,
                 recorder: IEmitRecorder,
                 args: ArgsTypes = None,
                 kwargs: KwargsTypes = None,
                 thread_workers: int = None):
        self._target = target  # task function
        self._args = () if not args else args
        self._kwargs = {} if not kwargs else kwargs
        self._thread_workers = thread_workers  # set ThreadPoolExecutor of max_workers

        self._counter = counter  # async counter
        self._tasks = tasks  # task queue
        self._recorder = recorder

    @property
    def target(self):
        return self._target

    @property
    def recorder(self):
        return self._recorder

    async def start(self):
        target = self.target
        async for count in self._counter:
            self._put_to_queue(target)

        # 交由消费侧
        result = await self.join()
        return result

    async def join(self):
        _join = self._join(self.recorder, self._tasks)
        return await _join.join()

    def _join(self, recorder, task):
        return WorkerJoin(recorder, task)

    def _put_to_queue(self, target: CoroOrFunction) -> None:
        task = self._to_task(
            target,
            self._args,
            self._kwargs,
            self._thread_workers
        )
        self._add_task(task)

    def _add_task(self, task):
        self._tasks.put(task)

    def _to_task(self,
                 coro_or_func: CoroOrFunction,
                 args: ArgsTypes = None,
                 kwargs: KwargsTypes = None,
                 max_workers: int = None):
        factory = TaskFactory(
            coro_or_func,
            args,
            kwargs,
            max_workers
        )
        return factory.create_task()
