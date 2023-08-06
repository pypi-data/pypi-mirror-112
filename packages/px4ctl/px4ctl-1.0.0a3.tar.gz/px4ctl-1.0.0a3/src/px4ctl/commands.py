from __future__ import annotations

from asyncio import sleep
from typing import Awaitable, Optional, TypeVar, Generic, Callable, Generator, Any


_T = TypeVar("_T")
_Thunk = Callable[[], Awaitable[_T]]


class CommandError(Exception):
    pass


class Command(Generic[_T]):
    def __init__(self, cmd: _Thunk[_T], retries: int = 3, delay_ms: Optional[int] = None):
        self.cmd = cmd
        self.retries = retries
        self.delay = delay_ms

    async def run(self) -> _T:
        for ntry in range(0, self.retries):
            try:
                return await self.cmd()
            except Exception as ex:
                if ntry == self.retries - 1:
                    raise CommandError(ex)
                else:
                    if self.delay is not None:
                        await sleep(self.delay / 1000)
                    continue

        raise RuntimeError()

    def __await__(self) -> Generator[Any, None, _T]:
        return self.run().__await__()


def cmd(func: _Thunk[_T]) -> Awaitable[_T]:
    return Command(func)
