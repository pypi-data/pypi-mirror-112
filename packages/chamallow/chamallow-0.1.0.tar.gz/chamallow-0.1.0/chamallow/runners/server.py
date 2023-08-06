import asyncio
import logging
from enum import Enum
from multiprocessing import Process
from multiprocessing.connection import Connection
from typing import List, Optional

from ..backends import server_backend
from ..helpers import start_async
from ..messages import Func, ResultRequest
from ..settings import settings
from ..states import ClientState, CoreState

logger = logging.getLogger(__name__)


class ServerRunner(Process):
    def __init__(
        self,
        *args,
        conn: Connection,
        client_conns: Optional[List[Connection]] = None,
        **kwargs
    ):
        """[summary]

        Arguments:
            Process {[type]} -- [description]
            client_conns {Optional[List[Connection]]} -- [description]
            conn {Connection} -- [description]
        """
        super().__init__(*args, **kwargs)
        self.client_conns = client_conns
        self.conn = conn

    async def _arun(self):
        """[summary]"""
        msg = None

        while not isinstance(msg, Enum) and msg != CoreState.EXITING:
            msg = self.conn.recv()
            logger.debug("msg: %s", msg)

            if isinstance(msg, Func):
                state = None

                while state != ClientState.DONE:
                    state = await server_backend.async_it(self, msg)
                    logger.debug("state: %s", state)
                    await asyncio.sleep(settings.polling_interval * 0.001)

            elif isinstance(msg, ResultRequest):
                self.conn.send(await server_backend.result(self, msg.id))

        server_backend.close()

    def run(self):
        """[summary]"""
        start_async(self._arun)
