import logging

from .context import context


def log_init():
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    fmt = logging.Formatter('%(message)s')
    console.setFormatter(fmt)

    logger = logging.getLogger("ssh out")
    logger.addHandler(console)
    logger.setLevel(logging.DEBUG)

    if 'log_file' in context:
        file_log = logging.FileHandler(context.log_file)
        file_log.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(levelname)s] %(asctime)s  %(filename)s %(lineno)d : %(message)s')
        file_log.setFormatter(fmt)
        logger.addHandler(file_log)

    return logger


logger = log_init()


def get_logger():
    return logger
