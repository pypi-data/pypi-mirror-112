# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Union

from f1z1_async_runner import create_runner, start

from ..components import IEmitTaskSet, IEmitRecorder
from .base import IWorker, IWorkerGroup, IWorkerMaster

WorkerTypes = Union[IWorker, IWorkerGroup]


class EmitWorkerMaster(IWorkerMaster):

    def __init__(self, task_set: IEmitTaskSet, recorder: IEmitRecorder):
        self._set = task_set
        self._recorder = recorder

    @property
    def task_set(self):
        return self._set

    @property
    def recorder(self) -> IEmitRecorder:
        return self._recorder

    def add(self, worker_or_group) -> None:
        """
        add worker or worker group -> set
        :param worker_or_group:
        :return:
        """
        self._check_worker(worker_or_group)
        self.task_set.add(worker_or_group)

    def run(self, worker_or_group: WorkerTypes = None) -> IEmitRecorder:
        """
        run worker or worker group
        :param worker_or_group:
        :return:
        """
        runner = create_runner(worker_or_group.start())
        return start(runner)

    def start(self) -> IEmitRecorder:
        """
        multi process start
        :return:
        """
        workers = self.task_set
        save = self.recorder.save

        with ProcessPoolExecutor(max_workers=2) as executor:
            # TODO: 暂时稳定
            fs = {executor.submit(self.run, worker) for worker in workers}
            for fut in as_completed(fs):
                save(fut.result())
        return self.recorder

    def _save(self, fut):
        self.recorder.save(fut.result())

    def _check_worker(self, worker):
        if all([
            not self._is_worker(worker),
            not self._is_worker_group(worker)
        ]):
            raise ValueError(
                f"worker need IWorker or IWorkerGroup, but got {type(worker).__name__}"
            )

    def _is_worker(self, value):
        return isinstance(value, IWorker)

    def _is_worker_group(self, value):
        return isinstance(value, IWorkerGroup)
