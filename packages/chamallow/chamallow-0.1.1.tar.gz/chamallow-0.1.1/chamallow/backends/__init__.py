from ..settings import settings

__all__ = (
    "client_backend",
    "server_backend",
)


def ClientBackend():
    if not settings.local:
        try:
            import zmq  # noqa

            from .zmq import ZMQClientBackend

            return ZMQClientBackend()
        except ImportError:
            pass
    # local
    from .process import ProcessClientBackend

    return ProcessClientBackend()


client_backend = ClientBackend()


def ServerBackend():
    if not settings.local:
        try:
            import zmq  # noqa

            from .zmq import ZMQServerBackend

            return ZMQServerBackend()
        except ImportError:
            pass
    # local
    from .process import ProcessServerBackend

    return ProcessServerBackend()


server_backend = ServerBackend()
