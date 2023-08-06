from typing import Any, Optional
from robot.api import logger
from .ElasticSearch import Elastic


# TODO Exemplo de classe, modelo inicial.
class LogToDriver:

    FORMAT = ""

    def __init__(self) -> None:
        self.el = Elastic()

    def _message(self, message: str, traceId: Optional[str] = None, **kwargs: Any):
        msg = message
        args = ""
        if traceId:
            msg = f"ID: {traceId} | {message}"
        for key, value in kwargs.items():
            args = f" {key}={value}"
        msg = f"{msg} | {args}" if kwargs else msg
        return msg

    def log_info(self, message: str, traceId: Optional[str] = None, **kwargs: Any):
        msg = self._message(message, traceId=traceId, **kwargs)
        logger.info(msg, html=True, also_console=True)
        self.el.publish(message, traceId=traceId, level="INFO", **kwargs)

    def log_warn(self, message: str, traceId: Optional[str] = None, **kwargs: Any):
        msg = self._message(message, traceId=traceId, **kwargs)
        logger.warn(msg, html=True)
        self.el.publish(message, traceId=traceId, level="WARN", **kwargs)

    def log_debug(self, message: str, traceId: Optional[str] = None, **kwargs: Any):
        msg = self._message(message, traceId=traceId, **kwargs)
        logger.debug(msg, html=True)
        self.el.publish(message, traceId=traceId, level="DEBUG", **kwargs)

    def log_error(self, message: str, traceId: Optional[str] = None, **kwargs: Any):
        msg = self._message(message, traceId=traceId, **kwargs)
        logger.error(msg, html=True)
        self.el.publish(message, traceId=traceId, level="ERROR", **kwargs)
