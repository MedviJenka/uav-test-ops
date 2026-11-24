import logfire
from typing import Any
from settings import Config, LogLevel


class Logger:
    """Thin wrapper around Logfire, configured once from settings.

    Messages are Logfire templates: pass values as keyword arguments so they are
    recorded as structured attributes, e.g.
        log.fire('Connected: system id {system_id}', system_id=1)
    Logs always print to the console; they are also sent to Logfire Cloud
    only when LOGFIRE_TOKEN is set.
    """

    def __init__(self) -> None:
        token = Config.LOGFIRE_TOKEN.get_secret_value() or None
        logfire.configure(
            token=token,
            send_to_logfire='if-token-present',
            service_name=Config.LOGFIRE_SERVICE_NAME,
            environment=Config.LOGFIRE_ENVIRONMENT,
            console=logfire.ConsoleOptions(min_log_level=Config.LOG_LEVEL),
        )

    @staticmethod
    def fire(message: str, level: LogLevel = 'info', **attributes: Any) -> None:
        logfire.log(level, message, attributes=attributes)

    @staticmethod
    def span(message: str, **attributes: Any):
        """Group the logs inside a `with` block, e.g. one flight-check run."""
        return logfire.span(message, **attributes)


log = Logger()
