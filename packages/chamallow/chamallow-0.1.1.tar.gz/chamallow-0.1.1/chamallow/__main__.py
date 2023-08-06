import logging
import os
import sys
from argparse import ArgumentParser, Namespace
from typing import Any, Dict, Optional

import orjson

from .core import engine
from .helpers import run_func, start_async
from .logging import configure_logging
from .messages import Func, ResultRequest
from .readers import YamlReader

logger = logging.getLogger(__name__)


def parse_args() -> Namespace:
    """Parse command line options.

    Returns:
        Namespace -- command options to take into account
    """
    parser = ArgumentParser(description="Run Chamallow as client or server.")
    parser.add_argument("path", nargs="?")
    parser.add_argument(
        "--args", "-a", default="", help="Args to pass to first func, ex.: foo,bar"
    )
    parser.add_argument(
        "--kwargs", "-k", default="{}", help="Kwargs to pass to first func"
    )
    return parser.parse_args()


async def run_server(
    path: str,
    args: Optional[list] = None,
    kwargs: Optional[dict] = None,
):
    """[summary]

    Arguments:
        path {str} -- [description]

    Keyword Arguments:
        args {Optional[list]} -- [description] (default: {None})
        kwargs {Optional[dict]} -- [description] (default: {None})
    """
    reqs_registry = {}  # type: Dict[str, ResultRequest]

    def fetch_val(val: Any) -> Any:
        """[summary]

        Arguments:
            val {Any} -- [description]

        Returns:
            Any -- [description]
        """
        if isinstance(val, dict):
            if "_from" in val:
                return engine.result(reqs_registry[val["_from"]])

            elif "_from_args" in val:
                index = val["_from_args"]
                if isinstance(index, int) and index < len(args):
                    return args[index]
                else:
                    raise RuntimeError(f"invalid args index: {index}")

            elif "_from_env" in val:
                key = val["_from_env"]
                if key in os.environ:
                    return os.environ[key]
                else:
                    raise RuntimeError(f"env var not found: {key}")

            elif "_from_kwargs" in val:
                key = val["_from_kwargs"]
                if key in kwargs:
                    return kwargs[key]
                else:
                    raise RuntimeError(f"invalid kwargs key: {key}")
        return val

    async for funcs in YamlReader(path):
        for func_key, func_dict in funcs.items():
            when = [fetch_val(a) for a in func_dict.get("when", ())]
            if when and not all(when):
                continue

            func_args = [fetch_val(a) for a in func_dict.get("args", ())]
            func_kwargs = {
                k: fetch_val(v) for k, v in func_dict.get("kwargs", {}).items()
            }

            res_key = func_dict.get("register", func_key)
            tags = func_dict.get("tags", ())

            func = Func(
                name=func_dict["name"], args=func_args, kwargs=func_kwargs, tags=tags
            )
            reqs_registry[res_key] = ResultRequest(id=engine.run(func))


def run():
    """[summary]"""
    configure_logging()
    parsed_args = parse_args()
    try:
        engine.start()
        if parsed_args.path:
            _args = [a for a in parsed_args.args.split(",") if a]
            _kwargs = orjson.loads(parsed_args.kwargs)

            if os.path.exists(parsed_args.path):
                start_async(run_server, parsed_args.path, args=_args, kwargs=_kwargs)
            else:
                start_async(run_func, parsed_args.path, args=_args, kwargs=_kwargs)

            # always stop if path is specified
            engine.stop()
        # always run, work as client
        else:
            pass
    except KeyboardInterrupt:
        engine.stop()
    except RuntimeError as err:
        engine.stop()
        print(err)
        sys.exit(1)


if __name__ == "__main__":
    run()
