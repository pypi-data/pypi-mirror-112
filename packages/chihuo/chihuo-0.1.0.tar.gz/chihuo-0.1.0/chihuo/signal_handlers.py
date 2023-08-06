import logging
import asyncio
import functools
import signal

from .common import ChihuoType

logger = logging.getLogger(__name__)

IS_ON_TERM = False
IS_ON_INT = False


async def _wait_for_tasks(loop):
    logger.info("wait for futures to completed")

    while True:
        tasks = asyncio.all_tasks(loop)
        logger.warning("current tasks: %s", len(tasks))
        if len(tasks) <= 1:
            break
        await asyncio.sleep(1, loop)
        cancel_nonchihuo_tasks(loop)

    loop.stop()


def cancel_nonchihuo_tasks(loop):
    tasks = asyncio.all_tasks(loop)
    for task in tasks:
        if not hasattr(task, "ch_type"):
            task.cancel()


def wait_for_tasks(signum, frame, factories=None, loop=None):
    logger.info("handle signal %s: wait_for_tasks", signum)

    global IS_ON_TERM
    global IS_ON_INT
    if IS_ON_TERM or IS_ON_INT:
        return

    for factory in factories:
        factory.stop = True

    cancel_nonchihuo_tasks(loop)
    task = loop.create_task(_wait_for_tasks(loop))
    task.ch_type = ChihuoType.Handler

    IS_ON_TERM = True


def send_back_tasks(signum, frame, factories=None, loop=None):
    logger.info("handle signal %s: send_back_tasks", signum)

    global IS_ON_TERM
    global IS_ON_INT
    if IS_ON_TERM or IS_ON_INT:
        return

    for factory in factories:
        factory.stop = True
        factory._sendback_and_cancel_tasks()

    cancel_nonchihuo_tasks(loop)
    task = loop.create_task(_wait_for_tasks(loop))
    task.ch_type = ChihuoType.Handler

    IS_ON_INT = True


def set_signal_handlers(factories, loop):
    signal.signal(
        signal.SIGTERM,
        functools.partial(wait_for_tasks, factories=factories, loop=loop),
    )
    signal.signal(
        signal.SIGINT,
        functools.partial(send_back_tasks, factories=factories, loop=loop),
    )
