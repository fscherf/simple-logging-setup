import logging

from simple_logging_setup.terminal import journald_is_running
from simple_logging_setup.formatter import LogFormatter
from simple_logging_setup.filter import LogFilter

VERSION = (0, 0)
VERSION_STRING = '.'.join(str(i) for i in VERSION)

# state
_formatter = None
_filter = None


def setup(
        level='info',
        syslog_priorities='auto',
        loggers=None,
):

    global _formatter, _filter

    level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }[level.lower()]

    logging.basicConfig(level=level)

    # syslog priorities
    if syslog_priorities == 'always':
        syslog_priorities = True

    elif syslog_priorities == 'no':
        syslog_priorities = False

    elif syslog_priorities == 'auto':
        syslog_priorities = journald_is_running()

    # setup log formatting and log filtering
    log_formatter = LogFormatter(syslog_priorities=syslog_priorities)
    log_filter = LogFilter()

    for handler in logging.getLogger().root.handlers:
        handler.setFormatter(log_formatter)
        handler.addFilter(log_filter)

    # setup filtering
    loggers = loggers or []

    for logger_name in loggers:
        if logger_name.startswith('_'):
            log_filter.exclude(logger_name[1:])

        else:
            if logger_name.startswith('+'):
                logger_name = logger_name[1:]

            log_filter.include(logger_name)

