import logging
from enum import Enum
from hashlib import blake2b
from json.decoder import JSONDecodeError
from typing import NamedTuple

import orjson

from .exceptions import MessageException

logger = logging.getLogger(__name__)


class ErrorEnum(str, Enum):
    not_found = "not-found"

    @classmethod
    def from_value(cls, value: str) -> Enum:
        if value == "not-found":
            return cls.not_found
        else:
            raise MessageException


class Error(NamedTuple):
    id: str
    error: ErrorEnum

    @classmethod
    def from_json(cls, json_: bytes) -> object:
        return cls(
            **{
                k: ErrorEnum.from_value(v) if k == "error" else v
                for k, v in orjson.loads(json_).items()
            }
        )

    def to_json(self) -> bytes:
        return orjson.dumps(
            {k: v.value if k == "error" else v for k, v in self._asdict().items()}
        )


class RequestKindEnum(str, Enum):
    result = "result"
    run = "run"

    @classmethod
    def from_value(cls, value: str) -> Enum:
        if value == "result":
            return cls.result
        elif value == "run":
            return cls.run
        else:
            raise MessageException


class Request(NamedTuple):
    id: str
    kind: RequestKindEnum
    port: int
    tags: list

    @classmethod
    def from_json(cls, json_: bytes) -> object:
        try:
            return cls(
                **{
                    k: RequestKindEnum.from_value(v) if k == "kind" else v
                    for k, v in orjson.loads(json_).items()
                }
            )
        except (AttributeError, JSONDecodeError):
            raise TypeError

    def to_json(self) -> bytes:
        return orjson.dumps(
            {k: v.value if k == "kind" else v for k, v in self._asdict().items()}
        )


class Func(NamedTuple):
    name: str
    args: list
    kwargs: dict
    tags: list

    @classmethod
    def from_json(cls, json_: bytes) -> object:
        return cls(**orjson.loads(json_))

    def get_hash(self) -> str:
        return blake2b(self.to_json()).hexdigest()

    def to_json(self) -> bytes:
        return orjson.dumps(self._asdict())


class ResultRequest(NamedTuple):
    id: str

    @classmethod
    def from_json(cls, json_: bytes) -> object:
        return cls(**orjson.loads(json_))

    def to_json(self) -> bytes:
        return orjson.dumps(self._asdict())
