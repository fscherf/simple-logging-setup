from traceback import format_exception
from textwrap import indent
import threading
import datetime
import logging
import socket
import os

from simple_logging_setup.terminal import (
    terminal_supports_colors,
    colors_are_enabled,
)

try:
    # syslog is only on unix based systems available
    import syslog

    SYSLOG_IS_AVAILABLE = True

except ImportError:
    SYSLOG_IS_AVAILABLE = False


def get_syslog_priority(levelno):
    if levelno <= logging.DEBUG:
        return syslog.LOG_DEBUG

    elif levelno <= logging.INFO:
        return syslog.LOG_INFO

    elif levelno <= logging.WARNING:
        return syslog.LOG_WARNING

    elif levelno <= logging.ERROR:
        return syslog.LOG_ERR

    elif levelno <= logging.CRITICAL:
        return syslog.LOG_CRIT

    return syslog.LOG_ALERT


class LogFormatter(logging.Formatter):
    def __init__(self, *args, syslog_priorities=False, **kwargs):
        super().__init__(*args, **kwargs)

        self.syslog_priorities = SYSLOG_IS_AVAILABLE and syslog_priorities

        self.colors_enabled = (
            terminal_supports_colors() and
            colors_are_enabled()
        )

    def format(self, record):
        current_thread_name = threading.current_thread().name

        # format record string
        time_stamp = datetime.datetime.fromtimestamp(record.created)
        time_stamp_str = time_stamp.strftime('%H:%M:%S.%f')

        record_string = '{}{} {}{} {} {} {}'.format(
            current_thread_name,
            (30 - len(current_thread_name)) * ' ',

            record.levelname,
            (8 - len(record.levelname)) * ' ',

            time_stamp_str,
            record.name,
            record.getMessage(),
        )

        # format exc_info
        if record.exc_info:
            record_string = '{}\n{}'.format(
                record_string,
                indent(
                    ''.join(format_exception(*record.exc_info))[:-1],
                    prefix='  ',
                ),
            )

        # syslog priorities
        if self.syslog_priorities:
            syslog_priority = get_syslog_priority(record.levelno)

            record_string = f'<{syslog_priority}>{record_string}'

        # colors
        if record.levelname == 'INFO' or not self.colors_enabled:
            return record_string

        RED = '31'
        YELLOW = '33'
        WHITE = '37'
        GREEN = '32'
        BACKGROUND_RED = '41'

        BRIGHT = '1'

        style = ''
        background = ''
        color = ''

        if record.levelname == 'DEBUG':
            style = ''
            background = ''
            color = GREEN

        elif record.levelname == 'WARNING':
            style = ''
            background = ''
            color = YELLOW

        elif record.levelname == 'ERROR':
            style = BRIGHT
            background = ''
            color = RED

        elif record.levelname == 'CRITICAL':
            style = BRIGHT
            background = BACKGROUND_RED
            color = WHITE

        if style:
            color = f';{color}'

        if background and color:
            background = f';{background}'

        return f'\033[{style}{color}{background}m{record_string}\033[00m'

