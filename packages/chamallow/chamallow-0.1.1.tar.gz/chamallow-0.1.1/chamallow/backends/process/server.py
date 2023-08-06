import logging
from random import randint
from typing import Any, Dict

import orjson

from ...messages import Error, ErrorEnum, Func, Request, RequestKindEnum
from ...states import ClientState

logger = logging.getLogger(__name__)


class ProcessServerBackend:
    _client_indexes: Dict[str, int] = {}

    def close(self):
        pass

    async def async_it(self, runner: Any, func: Func) -> ClientState:
        """[summary]

        Arguments:
            runner {Any} -- [description]
            func {Func} -- [description]

        Returns:
            ClientState -- [description]
        """
        if not runner.client_conns:
            logger.debug("No client")
            return ClientState.NO_CLIENT

        func_id = func.get_hash()
        # get a client conn randomly
        x = randint(0, len(runner.client_conns) - 1)
        self._client_indexes[func_id] = x
        conn = runner.client_conns[x]
        # send request info to client
        request = Request(id=func_id, kind=RequestKindEnum.run, port=0, tags=func.tags)
        conn.send(request.to_json())
        # send func
        conn.send(func.to_json())
        # done
        return ClientState.DONE

    async def result(self, runner: Any, func_id: str) -> Dict[Any, Any]:
        """[summary]

        Arguments:
            runner {Any} -- [description]
            func_id {str} -- [description]

        Returns:
            Dict[Any, Any] -- [description]
        """
        # not found
        if func_id not in self._client_indexes:
            return Error(id=func_id, error=ErrorEnum.not_found)._asdict()
        # get previously use client conn
        x = self._client_indexes[func_id]
        conn = runner.client_conns[x]
        # send conn info
        request = Request(id=func_id, kind=RequestKindEnum.result, port=0, tags=[])
        conn.send(request.to_json())
        # retrieve result
        return orjson.loads(conn.recv())
