from abc import ABC, abstractmethod

from lodis_py.client import AsyncLodisClient


class Wrapper(ABC):
    @abstractmethod
    async def exists(self, key):
        """Check whether the key exists in the queue"""
        raise NotImplementedError

    @abstractmethod
    async def push_left(self, key, value):
        """Add tasks to the left of the queue"""
        raise NotImplementedError

    @abstractmethod
    async def pushnx_left(self, key, value):
        """Add tasks to the left of the queue only if item does not exists in the queue"""
        raise NotImplementedError

    @abstractmethod
    async def push(self, key, value):
        """Add tasks to the right of the queue"""
        raise NotImplementedError

    @abstractmethod
    async def pushnx(self, key, value):
        """Add tasks to the right of the queue only if item does not exists in the queue"""
        raise NotImplementedError

    @abstractmethod
    async def pop_left(self):
        """Take out an task from the left of the queue"""
        raise NotImplementedError

    @abstractmethod
    async def pop(self):
        """Take out an task from the right of the queue"""
        raise NotImplementedError

    @abstractmethod
    async def finish(self, key):
        """Set the task which has the key to finished"""
        raise NotImplementedError

    @abstractmethod
    async def finished(self, key):
        """Check whether a task is finished"""
        raise NotImplementedError

    @abstractmethod
    async def unfinish(self, key):
        """Set the task which has the key to unfinished"""
        raise NotImplementedError


class LodisWrapper(Wrapper):
    def __init__(self, namespace, ip, port, loop=None):
        self._lodis = AsyncLodisClient(namespace, ip, port, loop=loop)

    # ArrayMap
    async def exists(self, key):
        return await self._lodis.aexists(key)

    async def push_left(self, *pairs):
        return await self._lodis.alpush(*pairs)

    async def pushnx_left(self, *pairs):
        return await self._lodis.alpushnx(*pairs)

    async def push(self, *pairs):
        return await self._lodis.arpush(*pairs)

    async def pushnx(self, *pairs):
        return await self._lodis.arpushnx(*pairs)

    async def pop_left(self):
        return await self._lodis.alpop()

    async def pop(self):
        return await self._lodis.arpop()

    # Map
    async def finish(self, *keys):
        pairs = [(key, b"") for key in keys]
        return await self._lodis.hmset(*pairs)

    async def finished(self, key):
        return await self._lodis.hexists(key)

    async def unfinish(self, key):
        return await self._lodis.hdel(key)
