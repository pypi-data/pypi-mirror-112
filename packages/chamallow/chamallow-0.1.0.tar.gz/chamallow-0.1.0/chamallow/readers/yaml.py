import logging
from typing import Any, Dict, List

import aiofiles
from cached_property import cached_property
from yaml import safe_load as load_yaml

logger = logging.getLogger(__name__)


def depends_from(values: List[Any]) -> List[str]:
    """[summary]

    Arguments:
        values {List[Any]} -- [description]

    Returns:
        List[str] -- [description]
    """
    return [v["_from"].strip() for v in values if isinstance(v, dict) and "_from" in v]


class YamlReader:
    def __init__(self, yaml_path: str):
        """[summary]

        Arguments:
            yaml_path {str} -- [description]
        """
        self.yaml_path = yaml_path

    @cached_property
    async def yaml(self) -> Dict[str, dict]:
        """[summary]

        Returns:
            Dict[str, dict] -- [description]
        """
        async with aiofiles.open(self.yaml_path) as f:
            return load_yaml(await f.read())

    def __aiter__(self):
        self.returned = dict()  # type: Dict[str, dict]
        return self

    async def __anext__(self) -> Dict[str, dict]:
        """[summary]

        Raises:
            StopAsyncIteration: [description]

        Returns:
            Dict[str, dict] -- [description]
        """
        next_funcs = {}

        for func_key, func_dict in (await self.yaml).items():
            depends = depends_from(
                func_dict.get("args", []) + list(func_dict.get("kwargs", {}).values())
            )

            if func_key not in self.returned and all(
                (n in self.returned) for n in depends
            ):
                next_funcs[func_key] = func_dict

        self.returned.update(next_funcs)

        if next_funcs:
            return next_funcs
        else:
            raise StopAsyncIteration
