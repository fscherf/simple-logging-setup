import logging

from simple_logging_setup.platform import journald_is_running
from simple_logging_setup.formatter import LogFormatter
from simple_logging_setup.filter import LogFilter

from simple_logging_setup.configuration import (
    include_logger,
    exclude_logger,
    get_value,
    configure,
)

VERSION = (0, 0)
VERSION_STRING = '.'.join(str(i) for i in VERSION)

# state
_formatter = None
_filter = None


def setup(loggers=None, **configuration):
    configure(**configuration)

    logging.basicConfig(level=get_value('level'))

    # setup log formatting and log filtering
    log_formatter = LogFormatter()
    log_filter = LogFilter()

    for handler in logging.getLogger().root.handlers:
        handler.setFormatter(log_formatter)
        handler.addFilter(log_filter)

    # setup filtering
    loggers = loggers or []

    for logger_name in loggers:
        if logger_name.startswith('_'):
            exclude_logger(logger_name[1:])

        else:
            if logger_name.startswith('+'):
                logger_name = logger_name[1:]

            include_logger(logger_name)

