import os
import logging

DEFAULT_FMT = "%(asctime)-15s | %(levelname)s | %(module)s: %(message)s"
DEFAULT_FILENAME = "log/log.log"


def get_logger(
    name=None,
    fmt=DEFAULT_FMT,
    filename=DEFAULT_FILENAME,
    stream=None,
    level=logging.INFO,
):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if filename:
        dirt = os.path.dirname(filename)
        if dirt and not os.path.exists(dirt):
            os.makedirs(dirt)

        handler = logging.FileHandler(filename)
    else:
        handler = logging.StreamHandler(stream=stream)

    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)

    return logger
