import argparse
import logging

from simple_logging_setup import setup


# parse command line
parser = argparse.ArgumentParser()

parser.add_argument(
    '-l',
    '--log-level',
    choices=['debug', 'info', 'warn', 'error', 'critical'],
    default='info',
)

parser.add_argument(
    '--loggers',
    type=str,
    nargs='+',
)

parser.add_argument(
    '--show-time-stamps',
    action='store_true',
)

args = parser.parse_args()

# setup logging
setup(
    level=args.log_level,
    loggers=args.loggers,
    show_time_stamp=args.show_time_stamps,
)

# run test
logger = logging.getLogger('simple-logging-setup')

logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('warning message')
logger.critical('critical message')

logging.info('info logger message')
logging.warning('warning logger message')


try:
    a = 1 / 0

except Exception:
    logger.exception('exception')
