from traceback import format_exception
from textwrap import indent
import threading
import datetime
import logging

from simple_logging_setup.configuration import _configuration

try:
    import syslog

except ImportError:
    pass


class LogFormatter(logging.Formatter):
    def get_syslog_priority(self, levelno):
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

    def color_record_string(self, record, record_string):
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

    def format(self, record):
        record_string = ''

        # syslog priority
        if _configuration['syslog_priorities']:
            syslog_priority = self.get_syslog_priority(record.levelno)

            record_string = f'<{syslog_priority}>{record_string}'

        # thread name
        if _configuration['show_thread_name']:
            current_thread_name = threading.current_thread().name
            spacing = (30 - len(current_thread_name)) * ' '

            record_string = f'{record_string}{current_thread_name}{spacing} '

        # level
        if _configuration['show_level_name']:
            spacing = (8 - len(record.levelname)) * ' '

            record_string = f'{record_string}{record.levelname}{spacing} '

        # time stamp
        if _configuration['show_time_stamp']:
            time_stamp = datetime.datetime.fromtimestamp(record.created)
            time_stamp_str = time_stamp.strftime('%Y/%m/%d %H:%M:%S.%f')

            record_string = f'{record_string}{time_stamp_str} '

        # logger name
        if (_configuration['show_logger_name'] and
                record.name not in _configuration['filter_logger_names']):

            record_string = f'{record_string}{record.name}: '

        # message
        record_string = f'{record_string}{record.getMessage()}'

        # traceback
        if record.exc_info:
            record_string = '{}\n{}'.format(
                record_string,
                indent(
                    ''.join(format_exception(*record.exc_info))[:-1],
                    prefix='  ',
                ),
            )

        # colors
        if record.levelname == 'INFO' or not _configuration['colors']:
            return record_string

        return self.color_record_string(
            record=record,
            record_string=record_string,
        )
