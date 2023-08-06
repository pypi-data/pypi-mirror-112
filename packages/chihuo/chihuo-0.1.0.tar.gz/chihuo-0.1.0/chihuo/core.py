import logging
import asyncio

from .loop import ChihuoLoop
from .signal_handlers import set_signal_handlers

logger = logging.getLogger(__name__)


def run(*classes):
    if not classes:
        logger.error("No provide factory class")

    assert classes, "No provide factory class"

    factories = []
    for clz in classes:
        if type(clz) is not type:
            raise TypeError("factory must be a class")
        if not issubclass(clz, ChihuoLoop):
            raise TypeError("factory must be a subclass of ChihuoLoop")
        if clz.NAME is None:
            raise TypeError("factory.NAME must be given")

        factories.append(clz())

    logger.info("Find factories: %s", [factory.NAME for factory in factories])

    loop = asyncio.get_event_loop()
    set_signal_handlers(factories, loop)

    for factory in factories:
        factory._run()

    loop.run_forever()
