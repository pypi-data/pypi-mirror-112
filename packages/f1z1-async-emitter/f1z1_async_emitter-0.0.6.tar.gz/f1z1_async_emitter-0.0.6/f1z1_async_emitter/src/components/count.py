# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common import is_validators

from .base import IAwaitSpeed, IAsyncCountGenerator, Size


class CountGenerator(IAsyncCountGenerator):
    """
    count generator
    """

    def __init__(self, speed: IAwaitSpeed, maxsize: Size = None):
        self._speed = speed
        self._maxsize = self._computed_maxsize(maxsize)

    @property
    def maxsize(self):
        return self._maxsize

    async def __aiter__(self):
        for _, number in enumerate(self._maxsize):
            yield number
            await self._speed

    def _computed_maxsize(self, maxsize: Size):
        minsize = 2 ** 31
        if is_validators.is_int(maxsize):
            minsize = abs(maxsize)
        return range(minsize)
