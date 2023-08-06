# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import as_completed

from ..components import IEmitTaskQueue, IEmitRecorder
from .base import IWorkerJoin


class WorkerJoin(IWorkerJoin):

    def __init__(self,
                 recorder: IEmitRecorder,
                 task: IEmitTaskQueue):
        self._recorder = recorder
        self._task = task

    @property
    def recorder(self):
        return self._recorder

    @property
    def task(self):
        return self._task

    async def join(self) -> IEmitRecorder:
        for _, task in enumerate(as_completed(self.task)):
            await self.save(task)
        return self.recorder

    async def save(self, task):
        result = await task
        self.recorder.save(result)
