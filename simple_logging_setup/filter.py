from simple_logging_setup.configuration import _configuration

import logging


class LogFilter(logging.Filter):
    def filter(self, record):
        if record.name in _configuration['exclude']:
            return False

        if (_configuration['include'] and
                record.name not in _configuration['include']):

            return False

        return True
