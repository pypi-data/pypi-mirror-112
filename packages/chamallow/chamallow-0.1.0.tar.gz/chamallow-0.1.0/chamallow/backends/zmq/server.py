import logging
from contextlib import contextmanager
from typing import Any, Dict, Generator, Tuple

import orjson
import zmq
import zmq.asyncio
from cached_property import cached_property

from ...messages import Func, Request, RequestKindEnum
from ...settings import settings
from ...states import ClientState
from .common import socket_poller

logger = logging.getLogger(__name__)


@contextmanager
def bind_pair_socket() -> Generator[Tuple[zmq.asyncio.Socket, int], None, None]:
    """[summary]

    Yields:
        Tuple[zmq.asyncio.Socket, int] -- [description]
    """
    pair_socket = zmq.asyncio.Context().socket(zmq.PAIR)
    port = pair_socket.bind_to_random_port(
        "tcp://*",
        min_port=49152,
        max_port=49151 + settings.number_of_result_clients,
    )
    logger.debug("bind pair: %s", f"tcp://*:{port}")

    yield (pair_socket, port)

    pair_socket.close()
    logger.debug("pair closed")


class MessageIterator:
    """[summary]"""

    def __init__(self, pair_socket: zmq.asyncio.Socket, poller: zmq.asyncio.Poller):
        """[summary]

        Arguments:
            pair_socket {zmq.asyncio.Socket} -- [description]
            poller {zmq.asyncio.Poller} -- [description]
        """
        self.pair_socket = pair_socket
        self.poller = poller

    def __aiter__(self):
        return self

    async def __anext__(self) -> str:
        """[summary]

        Returns:
            str -- [description]
        """
        msg = None
        while not msg:
            socks = dict(await self.poller.poll(timeout=settings.polling_interval))
            if self.pair_socket in socks and socks[self.pair_socket] == zmq.POLLIN:
                msg = (await self.pair_socket.recv()).decode()
        return msg


class ZMQServerBackend:
    @cached_property
    def socket(self) -> zmq.asyncio.Socket:
        """[summary]

        Returns:
            zmq.asyncio.Socket -- [description]
        """
        socket = zmq.asyncio.Context().socket(zmq.PUSH)
        socket.bind(f"tcp://*:{settings.connect_port}")
        logger.debug("push socket ready")
        return socket

    def close(self):
        """[summary]"""
        self.socket.close()
        logger.debug("closed")

    async def async_it(self, runner: Any, func: Func) -> ClientState:
        """[summary]

        Arguments:
            runner {ServerRunner} -- [description]
            func {Func} -- [description]

        Returns:
            ClientState -- [description]
        """
        state = ClientState.UNKNOWN

        with bind_pair_socket() as (pair_socket, port), socket_poller(
            pair_socket
        ) as poller:
            request = Request(
                id=func.get_hash(), kind=RequestKindEnum.run, port=port, tags=func.tags
            )
            logger.debug("request: %s", request)
            # broadcast request
            await self.socket.send(request.to_json())
            # poll for states
            async for msg in MessageIterator(pair_socket, poller):
                logger.debug("msg: %s", msg)
                if msg == ClientState.DONE.value:
                    state = ClientState.DONE
                    break

                elif msg == ClientState.NOT_MATCH.value:
                    state = ClientState.NOT_MATCH
                    break

                elif msg == ClientState.HELO.value:
                    await pair_socket.send(func.to_json())
                    logger.debug("func sent")

        return state

    async def result(self, runner: Any, func_id: str) -> Dict[Any, Any]:
        """[summary]

        Arguments:
            runner {ServerRunner} -- [description]
            func_id {str} -- [description]

        Returns:
            Dict[Any, Any] -- [description]
        """
        with bind_pair_socket() as (pair_socket, port), socket_poller(
            pair_socket
        ) as poller:
            request = Request(
                id=func_id, kind=RequestKindEnum.result, port=port, tags=[]
            )
            logger.debug("request: %s", request)
            # broadcast request
            await self.socket.send(request.to_json())
            # poll for result
            async for msg in MessageIterator(pair_socket, poller):
                logger.debug("msg: %s", msg)
                break

        return orjson.loads(msg)
