import logging
from multiprocessing.connection import Connection
from typing import Any, AsyncGenerator, Dict

import orjson

from ...helpers import run_func
from ...messages import Request
from ...states import CoreState

logger = logging.getLogger(__name__)


class ProcessClientBackend:
    async def aiter_requests(self, conn: Connection) -> AsyncGenerator[object, None]:
        """[summary]

        Arguments:
            conn {Connection} -- [description]

        Yields:
            Request -- [description]
        """
        while True:
            msg = conn.recv()
            logger.debug("msg: %s", msg)
            if msg == CoreState.EXITING:
                break
            else:
                try:
                    yield Request.from_json(msg)
                except TypeError:
                    logger.warning("invalid message: %s", msg)

    async def async_it(self, conn: Connection, request: Request) -> Dict[Any, Any]:
        """[summary]

        Arguments:
            conn {Connection} -- [description]
            request {Request} -- [description]

        Returns:
            Dict[Any, Any] -- [description]
        """
        run_data = orjson.loads(conn.recv())
        logger.debug("run data: %s", run_data)
        return await run_func(**run_data)

    async def not_match(self, conn: Connection, request: Request):
        raise NotImplementedError

    async def result(self, conn: Connection, request: Request, result: Dict[Any, Any]):
        """[summary]

        Arguments:
            conn {Connection} -- [description]
            request {Request} -- [description]
            result {Dict[Any, Any]} -- [description]
        """
        conn.send(result)
        logger.debug("result sent")
