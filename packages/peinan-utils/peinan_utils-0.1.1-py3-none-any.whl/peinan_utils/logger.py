import sys
from loguru import logger


def get_logger(sink=sys.stderr, level='DEBUG') -> logger:
    logger.level('TRACE',    icon='TRA')
    logger.level('DEBUG',    icon='DBG')
    logger.level('INFO',     icon='INF')
    logger.level('SUCCESS',  icon='SCS')
    logger.level('WARNING',  icon='WRN')
    logger.level('ERROR',    icon='ERR')
    logger.level('CRITICAL', icon='CRT')

    log_format = (
        '<level>{level.icon}</level> <b>{time:YYMMDDtHHmmss}</b>'
        ' | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>'
        ' | <level>{message}</level>'
    )

    logger.remove()
    logger.add(
        sink, format=log_format,
        filter=None, colorize=None, serialize=False, backtrace=True,
        diagnose=True, enqueue=False, catch=True, level=level
    )

    return logger


if __name__ == '__main__':
    l = get_logger()
    levels = ['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
    for level in levels:
        l.log(level, f'This is {level} level message.')
