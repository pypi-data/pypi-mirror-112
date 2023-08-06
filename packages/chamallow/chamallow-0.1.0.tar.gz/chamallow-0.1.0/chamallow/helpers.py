import asyncio
import inspect
import signal
from functools import partial
from typing import Any, Callable, Optional

from .exceptions import GracefulExit


def import_func(import_str: str) -> Callable:
    """[summary]

    Arguments:
        import_str {str} -- [description]

    Returns:
        Callable -- [description]
    """
    module_name, func_name = str(import_str).rsplit(".", 1)
    module = __import__(module_name, globals(), locals(), [func_name])
    return getattr(module, func_name)


async def run_func(
    name: str,
    args: Optional[list] = (),
    kwargs: Optional[dict] = None,
    **kw,
) -> Any:
    """[summary]

    Arguments:
        name {str} -- [description]

    Keyword Arguments:
        args {Optional[list]} -- [description] (default: {None})
        kwargs {Optional[dict]} -- [description] (default: {None})

    Returns:
        Any -- [description]
    """
    f = import_func(name)
    f = getattr(f, "__wrapped__", f)
    f = partial(f, *args, **(kwargs or {}))
    if inspect.iscoroutinefunction(f):
        return await f()
    elif inspect.isgeneratorfunction(f):
        return list(x for x in f())
    elif inspect.isasyncgenfunction(f):
        return [x async for x in f()]
    else:
        return f()


def start_async(func: Callable, *args, **kwargs):
    """[summary]

    Arguments:
        func {Callable} -- [description]

    Raises:
        GracefulExit: [description]

    Returns:
        Any -- [description]
    """
    f = partial(func, *args, **kwargs)
    loop = asyncio.get_event_loop()

    # already running
    if loop.is_running():
        return asyncio.run(f())

    def raise_graceful_exit(*_, **__):
        loop.stop()
        raise GracefulExit()

    for s in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM):
        signal.signal(s, raise_graceful_exit)

    try:
        loop.run_until_complete(f())
    except GracefulExit:
        pass
    finally:
        loop.close()
