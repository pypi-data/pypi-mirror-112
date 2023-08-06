import logging
from multiprocessing import Process
from multiprocessing.connection import Connection

import orjson
from aiocache import SimpleMemoryCache

from ..backends import client_backend
from ..helpers import start_async
from ..messages import Error, ErrorEnum, RequestKindEnum
from ..settings import settings

logger = logging.getLogger(__name__)


class ClientRunner(Process):
    def __init__(self, *args, conn=Connection, **kwargs):
        """[summary]

        Keyword Arguments:
            conn {[type]} -- [description] (default: {Connection})
        """
        super().__init__(*args, **kwargs)
        self.cache = SimpleMemoryCache(ttl=settings.cache_ttl)
        self.conn = conn

    async def _arun(self):
        """[summary]"""
        async for request in client_backend.aiter_requests(self.conn):
            logger.debug("request: %s", request)

            if request.kind == RequestKindEnum.result:
                if await self.cache.exists(request.id):
                    result = await self.cache.get(request.id)
                else:
                    result = Error(id=request.id, error=ErrorEnum.not_found).to_json()
                logger.debug("result: %s", result)
                await client_backend.result(self.conn, request, result)

            elif (
                not settings.local
                and request.tags
                and not settings.tags.intersection(request.tags)
            ):
                await client_backend.not_match(self.conn, request)

            elif request.kind == RequestKindEnum.run:
                result = await client_backend.async_it(self.conn, request)
                await self.cache.set(request.id, result, dumps_fn=orjson.dumps)
                logger.debug("cached result: %s", result)

    def run(self):
        """[summary]"""
        start_async(self._arun)
