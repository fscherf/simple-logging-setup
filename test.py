import logging

from simple_logging_setup import setup


setup(
    level='debug',
)

logger = logging.getLogger('simple-logging-setup')

logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('warning message')
logger.critical('critical message')


try:
    a = 1 / 0

except Exception:
    logger.exception('exception')

