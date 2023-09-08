import logging
from logging.config import dictConfig

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "app"
    LOG_FORMAT: str = "%(levelname)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    @property
    def logging_config(self):
        """Return the logging configuration dictionary."""
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": self.LOG_FORMAT,  # Changed "fmt" to "format"
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
            },
            "loggers": {
                self.LOGGER_NAME: {"handlers": ["default"], "level": self.LOG_LEVEL},
            },
        }


dictConfig(LogConfig().logging_config)  # Using the property to get the logging config


def logger():
    return logging.getLogger(LogConfig().LOGGER_NAME)
