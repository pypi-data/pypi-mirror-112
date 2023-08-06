import logging
from contextlib import asynccontextmanager, contextmanager
from multiprocessing.connection import Connection
from typing import Any, AsyncGenerator, Dict, Generator

import orjson
import zmq
import zmq.asyncio

from ...helpers import run_func
from ...messages import Request
from ...settings import settings
from ...states import ClientState, CoreState
from .common import socket_poller

logger = logging.getLogger(__name__)


@contextmanager
def connect_socket() -> Generator[zmq.asyncio.Socket, None, None]:
    """[summary]

    Yields:
        zmq.asyncio.Socket -- [description]
    """
    socket = zmq.asyncio.Context().socket(zmq.PULL)
    socket_addr = f"tcp://{settings.address}:{settings.connect_port}"
    socket.connect(socket_addr)
    logger.debug("connected to server: %s", socket_addr)

    yield socket

    socket.close()
    logger.debug("server socket closed")


@asynccontextmanager
async def connect_pair_socket(port: int) -> AsyncGenerator[zmq.asyncio.Socket, None]:
    """[summary]

    Arguments:
        port {int} -- [description]

    Yields:
        zmq.asyncio.Socket -- [description]
    """
    socket = zmq.asyncio.Context().socket(zmq.PAIR)
    socket_addr = f"tcp://{settings.address}:{port}"
    socket.connect(socket_addr)
    logger.debug("connected to pair: %s", socket_addr)

    yield socket

    socket.close()
    logger.debug("pair socket closed")


@asynccontextmanager
async def fetch_run_data(
    pair_socket: zmq.asyncio.Socket,
) -> AsyncGenerator[Dict[Any, Any], None]:
    """[summary]

    Arguments:
        pair_socket {zmq.asyncio.Socket} -- [description]

    Yields:
        Dict[Any, Any] -- [description]
    """
    await pair_socket.send(ClientState.HELO.value.encode())
    logger.debug("helo sent")

    yield orjson.loads(await pair_socket.recv())

    await pair_socket.send(ClientState.DONE.value.encode())
    logger.debug("done sent")


class ZMQClientBackend:
    async def aiter_requests(self, conn: Connection) -> AsyncGenerator[object, None]:
        """[summary]

        Arguments:
            conn {Connection} -- [description]

        Yields:
            Request -- [description]
        """
        with connect_socket() as socket, socket_poller(socket) as poller:
            state = None
            while state != CoreState.EXITING:
                if conn.poll(timeout=settings.polling_interval * 0.001):
                    state = conn.recv()
                    logger.debug("state: %s", state)
                    continue
                socks = dict(
                    await poller.poll(timeout=settings.polling_interval * 0.001)
                )
                if socket in socks and socks[socket] == zmq.POLLIN:
                    yield Request.from_json(await socket.recv())

    async def async_it(self, conn: Connection, request: Request) -> Dict[Any, Any]:
        """[summary]

        Arguments:
            conn {Connection} -- [description]
            request {Request} -- [description]

        Returns:
            Dict[Any, Any] -- [description]
        """
        async with connect_pair_socket(request.port) as socket, fetch_run_data(
            socket
        ) as run_data:
            logger.debug("run data: %s", run_data)
            return await run_func(**run_data)

    async def not_match(self, conn: Connection, request: Request):
        """[summary]

        Arguments:
            conn {Connection} -- [description]
            request {Request} -- [description]
        """
        async with connect_pair_socket(request.port) as socket:
            await socket.send(ClientState.NOT_MATCH.value.encode())
            logger.debug("not match sent")

    async def result(self, conn: Connection, request: Request, result: Dict[Any, Any]):
        """[summary]

        Arguments:
            conn {Connection} -- [description]
            request {Request} -- [description]
            result {Dict[Any, Any]} -- [description]
        """
        async with connect_pair_socket(request.port) as socket:
            await socket.send(result)
            logger.debug("result sent")
