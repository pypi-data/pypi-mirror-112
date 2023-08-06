import asyncio
import inspect
import random
import sys
import time
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar, Union, cast

FuncT = TypeVar("FuncT", bound=Callable[..., Any])


class BackoffAlg(ABC):
    """
    Abstract Class to define the Backoff Algorithm to use in retry api
    """

    @abstractmethod
    def get_sleep_time(self, attempt: int):
        """
        This function should return the delay time in seconds to wait
        before next retry.

        :param attempt: Specifies the current attempt number
        :type attempt: int
        """


class NoBackOff(BackoffAlg):
    def get_sleep_time(self, attempt: int):
        return 0


class RandomBackOff(BackoffAlg):
    def __init__(self, wait: float):
        self.wait = wait

    def get_sleep_time(self, attempt: int):
        return random.random() * self.wait


class ExpBackOff(BackoffAlg):
    def __init__(self, backoff_factor: float):
        self.backoff_factor = backoff_factor

    def get_sleep_time(self, attempt: int):
        return (2 ** attempt) * self.backoff_factor


class retry_with_backoff_on:
    def __init__(
        self,
        exc: Union[Exception, Type[Exception]],
        tries: Optional[int] = None,
        backoff_alg: Optional[BackoffAlg] = None,
    ):
        """
        Decorator to retry a function with backoff, if an exception `exc` occurs.
        Default backoff algorithm if not provided, will be `Random`BackOff`

        NOTE: Applying this decorator over generator function results in reinit'ing
        the generator object, whenever there is a retry.
        So on retry, items yielded before the exception might also be re-yielded
        CALLER has the responsibility to handle those situations

        NOTE: This decorator does not handle the situation in which the generator object
        is used as an argument. In that case, this simply retries with current state of
        generator, since it has no other way to re-init the generator object

        :param exc: Exception to catch.
        :type exc: Union[Exception, Type[Exception]]
        :param tries: Total number of executions. If not specified, retries forever
        :type tries: Optional[int]
        :param backoff_alg: Backoff Algorithm to calculate delay between tries
        :type backoff_alg: Optional[BackoffAlg]
        """
        self.exc = exc
        self.tries = tries or sys.maxsize
        self.backoff_alg = backoff_alg or RandomBackOff(wait=1)

    def _sleep(self, attempt: int):
        sleep_time = self.backoff_alg.get_sleep_time(attempt)
        if sleep_time:
            time.sleep(sleep_time)

    async def _async_sleep(self, attempt: int):
        sleep_time = self.backoff_alg.get_sleep_time(attempt)
        if sleep_time:
            await asyncio.sleep(sleep_time)

    def __call__(self, func: FuncT) -> FuncT:  # noqa: C901

        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def _async_wrapper(*args, **kwargs):
                for attempt in range(1, self.tries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except self.exc:
                        if attempt == self.tries:
                            raise
                    await self._async_sleep(attempt)

            return cast(FuncT, _async_wrapper)

        if inspect.isasyncgenfunction(func):

            @wraps(func)
            async def _async_gen_wrapper(*args, **kwargs):
                for attempt in range(1, self.tries + 1):
                    try:
                        async for i in func(*args, **kwargs):
                            yield i
                        break
                    except self.exc:
                        if attempt == self.tries:
                            raise
                    await self._async_sleep(attempt)

            return cast(FuncT, _async_gen_wrapper)

        if inspect.isgeneratorfunction(func):

            @wraps(func)
            def _sync_gen_wrapper(*args, **kwargs):
                for attempt in range(1, self.tries + 1):
                    try:
                        yield from func(*args, **kwargs)
                        break
                    except self.exc:
                        if attempt == self.tries:
                            raise
                    self._sleep(attempt)

            return cast(FuncT, _sync_gen_wrapper)

        @wraps(func)
        def _sync_wrapper(*args, **kwargs):
            for attempt in range(1, self.tries + 1):
                try:
                    return func(*args, **kwargs)
                except self.exc:
                    if attempt == self.tries:
                        raise
                self._sleep(attempt)

        return cast(FuncT, _sync_wrapper)
