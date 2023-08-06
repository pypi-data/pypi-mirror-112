import logging
from multiprocessing import Pipe
from multiprocessing.connection import Connection
from time import sleep
from typing import Any, Dict, List

from cached_property import cached_property

from .logging import configure_logging
from .messages import Func, ResultRequest
from .runners import ClientRunner, ServerRunner
from .settings import settings
from .states import CoreState

__all__ = ("engine",)

logger = logging.getLogger(__name__)


class Engine:
    @cached_property
    def clients(self) -> List[ClientRunner]:
        """[summary]

        Returns:
            List[ClientRunner] -- [description]
        """
        return list(ClientRunner(conn=c["child"]) for c in self.client_conns)

    @cached_property
    def client_conns(self) -> List[Dict[str, Connection]]:
        """[summary]

        Returns:
            List[Dict[str, Connection]] -- [description]
        """
        return list(
            dict(zip(("parent", "child"), Pipe()))
            for _ in range(settings.number_of_clients)
        )

    @cached_property
    def server(self) -> ServerRunner:
        """[summary]

        Returns:
            ServerRunner -- [description]
        """
        return ServerRunner(
            client_conns=[c["parent"] for c in self.client_conns],
            conn=self.server_conns["child"],
        )

    @cached_property
    def server_conns(self) -> Dict[str, Connection]:
        """[summary]

        Returns:
            Dict[str, Connection] -- [description]
        """
        return dict(zip(("parent", "child"), Pipe()))

    def result(self, result_request: ResultRequest) -> Dict[Any, Any]:
        """[summary]

        Arguments:
            result_request {ResultRequest} -- [description]

        Raises:
            RuntimeError: [description]

        Returns:
            Dict[Any, Any] -- [description]
        """
        logger.debug("result request: %s", result_request)
        for _ in range(settings.number_of_result_clients):
            self.server_conns["parent"].send(result_request)
            result = self.server_conns["parent"].recv()
            if not isinstance(result, dict) or "error" not in result:
                return result
            else:
                logger.error("Error: %s", result)
        else:
            raise RuntimeError

    def run(self, func: Func) -> str:
        """[summary]

        Arguments:
            func {Func} -- [description]

        Returns:
            str -- [description]
        """
        logger.debug("func: %s", func)
        self.server_conns["parent"].send(func)
        return func.get_hash()

    def start(self):
        """[summary]"""
        if settings.debug:
            configure_logging()

        for c in self.clients:
            c.start()
        self.server.start()

    def stop(self):
        """[summary]"""
        try:
            if "server" in self.__dict__:
                while self.server.is_alive():
                    self.server_conns["parent"].send(CoreState.EXITING)
                    sleep(settings.polling_interval * 0.001)

            if "clients" in self.__dict__:
                for x, c in enumerate(self.clients):
                    while c.is_alive():
                        conn = self.client_conns[x]["parent"]
                        conn.send(CoreState.EXITING)
                        sleep(settings.polling_interval * 0.001)
        except KeyboardInterrupt:
            pass

        if "server" in self.__dict__:
            self.server.is_alive() and self.server.join()

        if "clients" in self.__dict__:
            for c in self.clients:
                c.is_alive() and c.join()


engine = Engine()
