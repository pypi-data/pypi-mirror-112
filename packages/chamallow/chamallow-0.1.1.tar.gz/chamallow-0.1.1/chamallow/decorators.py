import sys
from functools import wraps
from typing import Any, Callable, Optional

from .core import engine
from .messages import Func, ResultRequest


class LazyResult:
    def __init__(self, func_id: Any):
        """[summary]

        Arguments:
            func_id {Any} -- [description]
        """
        self.func_id = func_id

    @property
    def _async_result(self) -> Any:
        """[summary]

        Returns:
            Any -- [description]
        """
        try:
            return engine.result(ResultRequest(id=self.func_id))
        except RuntimeError:
            sys.exit(1)

    def result(self) -> Callable:
        """[summary]

        Returns:
            Callable -- [description]
        """
        return self._async_result


def flow(tags: Optional[list] = None) -> Callable:
    """[summary]

    Keyword Arguments:
        tags {Optional[list]} -- [description] (default: {None})

    Returns:
        Callable -- [description]
    """

    def wrap(func: Callable) -> Callable:
        """[summary]

        Arguments:
            func {Callable} -- [description]

        Returns:
            Callable -- [description]
        """
        func_name = f"{func.__module__}.{func.__name__}"

        @wraps(func)
        def wrapped_f(*args, **kwargs) -> LazyResult:
            """[summary]

            Returns:
                LazyResult -- [description]
            """
            _args = [getattr(a, "_async_result", a) for a in (args or [])]
            _kwargs = {
                k: getattr(v, "_async_result", v) for k, v in (kwargs or {}).items()
            }
            f = Func(name=func_name, args=_args, kwargs=_kwargs, tags=(tags or []))
            return LazyResult(engine.run(f))

        return wrapped_f

    return wrap
