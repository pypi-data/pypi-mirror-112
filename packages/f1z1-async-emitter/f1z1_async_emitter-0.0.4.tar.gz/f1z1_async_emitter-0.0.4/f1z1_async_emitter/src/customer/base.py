# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import TypeVar

"""
消费侧接口
"""

T = TypeVar("T")


class IWorkerJoin(object):

    async def join(self, *args, **kwargs) -> T:
        raise NotImplementedError("NotImplemented .join() -> ")
