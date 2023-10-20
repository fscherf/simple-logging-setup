import logging

from simple_logging_setup.formatter import LogFormatter
from simple_logging_setup.filter import LogFilter

from simple_logging_setup.configuration import (
    include_logger,
    exclude_logger,
    _configuration,
    configure,
)

VERSION = (0, 3)
VERSION_STRING = '.'.join(str(i) for i in VERSION)

# state
_formatter = None
_filter = None


def setup(loggers=None, **configuration):

    # configuration
    configure(**configuration)

    logging.basicConfig(level=_configuration['level'])

    # if there are no colors available to distinguish records, the level name
    # has to be printed
    if not _configuration['colors']:
        _configuration['show_level_name'] = True

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
