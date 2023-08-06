from enum import Enum


class ClientState(Enum):
    DONE = "done"
    HELO = "helo"
    NO_CLIENT = "no-client"
    NOT_MATCH = "not-match"
    UNKNOWN = "unknown"


class CoreState(Enum):
    EXITING = "exiting"
