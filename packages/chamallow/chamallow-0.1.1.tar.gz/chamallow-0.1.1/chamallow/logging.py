import logging
import logging.config

from .settings import settings


def configure_logging():
    """[summary]"""
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": settings.log_format,
                    "datefmt": "%H:%M:%S",
                },
            },
            "handlers": {
                "console": {"class": "logging.StreamHandler", "formatter": "default"},
            },
            "root": {
                "handlers": ["console"],
                "level": "DEBUG" if settings.debug else "ERROR",
            },
        }
    )
