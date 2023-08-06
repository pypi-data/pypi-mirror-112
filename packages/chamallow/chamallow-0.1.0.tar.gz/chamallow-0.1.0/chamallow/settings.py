from cached_property import cached_property
from dynaconf import LazySettings


class Settings:
    def __init__(self):
        self._settings = LazySettings(
            ENVVAR_FOR_DYNACONF="CHAMALLOW_SETTINGS",
            ENVVAR_PREFIX_FOR_DYNACONF="CHAMALLOW",
        )

    @cached_property
    def address(self) -> str:
        return self._settings.get("ADDRESS", default="localhost")

    @cached_property
    def cache_ttl(self) -> int:
        return self._settings.get("CACHE_TTL", cast="@int", default=60)

    @cached_property
    def connect_port(self) -> int:
        return self._settings.get("CONNECT_PORT", cast="@int", default=5556)

    @cached_property
    def debug(self) -> bool:
        return self._settings.get("DEBUG", cast="@bool", default=False)

    @cached_property
    def local(self) -> bool:
        return self._settings.get("LOCAL", cast="@bool", default=False)

    @cached_property
    def log_format(self) -> str:
        return self._settings.get(
            "LOG_FORMAT",
            default=(
                "%(levelname)s %(asctime)s.%(msecs)03d %(process)d "
                "%(module)s.%(funcName)s:%(lineno)d %(message)s"
            ),
        )

    @cached_property
    def polling_interval(self) -> int:
        return self._settings.get("POLLING_INTERVAL", cast="@int", default=10)

    @cached_property
    def number_of_clients(self) -> int:
        return self._settings.get("NUMBER_OF_CLIENTS", cast="@int", default=2)

    @cached_property
    def number_of_remote_clients(self) -> int:
        return self._settings.get("NUMBER_OF_REMOTE_CLIENTS", cast="@int", default=0)

    @property
    def number_of_result_clients(self) -> int:
        return self.number_of_clients + self.number_of_remote_clients

    def _split_tags(self, tags_str: str) -> set:
        return set(filter(None, (t.strip() for t in tags_str.split(","))))

    @cached_property
    def tags(self) -> set:
        return self._split_tags(self._settings.get("TAGS", default=""))


settings = Settings()
