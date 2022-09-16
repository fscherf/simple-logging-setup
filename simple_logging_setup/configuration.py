import logging

from simple_logging_setup.platform import (
    terminal_supports_colors,
    journald_is_running,
    syslog_is_available,
    colors_are_enabled,
)


class ConfigurationError(Exception):
    pass


def get_value(name):
    return _configuration[name]


def parse_log_level(value):
    _value = value.lower().strip()

    values = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'warning': logging.WARN,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }

    if _value in values:
        return values[_value]

    raise ConfigurationError("invalid log level '{}'".format(value))


def parse_switch(value):

    # bool
    if isinstance(value, bool):
        return value

    # int
    if isinstance(value, int):
        if value == 0:
            return False

        elif value == 1:
            return True

    # string
    _value = value.lower().strip()

    values = {
        'true': True,
        'false': False,
        'on': True,
        'off': False,
        'yes': True,
        'no': False,
        '1': True,
        '0': False,
    }

    if _value in values:
        return values[_value]

    # invalid value
    raise ConfigurationError("invalid switch value '{}'".format(value))


def include_logger(name):
    _configuration['include'].append(name)


def exclude_logger(name):
    _configuration['exclude'].append(name)


def configure(**kwargs):
    for name, value in kwargs.items():

        # invalid name
        if name not in _configuration:
            raise ConfigurationError("invalid config name '{}'".format(name))

        # level
        if name == 'level':
            _configuration[name] = parse_log_level(value)

        # switches
        if name in ('syslog_priorities', ):
            _configuration[name] = parse_switch(value)


_configuration = {
    'level': parse_log_level('info'),
    'syslog_priorities': syslog_is_available() and journald_is_running(),
    'colors': terminal_supports_colors() and colors_are_enabled(),
    'include': [],
    'exclude': [],
}
