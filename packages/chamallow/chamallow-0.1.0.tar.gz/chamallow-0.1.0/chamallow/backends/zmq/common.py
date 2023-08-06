from contextlib import contextmanager
from typing import Generator

import zmq
import zmq.asyncio


@contextmanager
def socket_poller(
    socket: zmq.asyncio.Socket,
) -> Generator[zmq.asyncio.Poller, None, None]:
    """[summary]

    Yields:
        zmq.asyncio.Poller -- [description]
    """
    poller = zmq.asyncio.Poller()
    poller.register(socket, zmq.POLLIN)

    yield poller

    poller.unregister(socket)
