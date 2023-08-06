import asyncio
import logging
from functools import wraps

from .adapter import LodisWrapper, Wrapper

from .error import UnknownServer

logger = logging.getLogger(__name__)


def handle_exception(gen):
    @wraps(gen)
    async def wrapper(*args, **kwargs):
        while True:
            try:
                return await gen(*args, **kwargs)
            except Exception as err:
                logger.error("Server error: %s, future: %s", err, gen)
                await asyncio.sleep(2)

    return wrapper


class Server(Wrapper):
    def __init__(self, namespace, config, loop=None):
        self._namespace = namespace
        self._config = config
        self._loop = loop
        self._server = self._select_server(namespace, config, loop)

    def _select_server(self, namespace, config, loop=None):
        backend = config.backend
        if backend == "lodis":
            return LodisWrapper(namespace, config.ip, config.port, loop=loop)
        else:
            raise UnknownServer(backend)

    @handle_exception
    async def exists(self, key):
        return await self._server.exists(key)

    @handle_exception
    async def push_left(self, *pairs):
        return await self._server.push_left(*pairs)

    @handle_exception
    async def pushnx_left(self, *pairs):
        return await self._server.pushnx_left(*pairs)

    @handle_exception
    async def push(self, *pairs):
        return await self._server.push(*pairs)

    @handle_exception
    async def pushnx(self, *pairs):
        return await self._server.pushnx(*pairs)

    @handle_exception
    async def pop_left(self):
        return await self._server.pop_left()

    @handle_exception
    async def pop(self):
        return await self._server.pop()

    @handle_exception
    async def finish(self, *keys):
        return await self._server.finish(*keys)

    @handle_exception
    async def finished(self, key):
        return await self._server.finished(key)

    @handle_exception
    async def unfinish(self, key):
        return await self._server.unfinish(key)
