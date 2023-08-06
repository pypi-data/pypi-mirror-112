import traceback
import logging
import asyncio
import json as stdjson
import types

from .server import Server
from .common import SERVER_DEFAULT_CONFIG_PATH, ChihuoType, Direction
from .config import parse_server_config
from .util import make_ctrl_queue, serialize_json

logger = logging.getLogger(__name__)


class ChihuoLoop:
    """Chihuo async loop abstract class

    The class handles all asynchronous tasks which are created
    by the `make_task` method of its subclass.

    The class connects to a Chihuo server to persist all tasks.
    All running tasks are received from the backend server.
    So, for adding a task to the loop, subclass must use the
    `add_task` method to add the task to the backend server,
    then the loop can automaticly get a task from the backend
    server. The received task is passed to `make_task` to make
    an asynchronous generator which is added to the asynchronous
    loop.

    The backend server can be regarded as a bidirectional queue.

    Params:

    NAME: The unique project name (MUST BE ascii characters)
        It is the key to define the task queue of the project in
        backend server.

    CONCURRENCY: The number of all concurrent tasks

    SERVER_CONFIG: The configuration of the backend server
        It is a dict or a path to the configuration file.
        Default is the path 'chdb.config'
    """

    NAME = None
    CONCURRENCY = 1
    SERVER_CONFIG = SERVER_DEFAULT_CONFIG_PATH

    def __init__(self):
        if not self.NAME:
            logger.warning("NAME is missing")

        assert self.NAME, "NAME is missing"
        assert self.CONCURRENCY > 0, "CONCURRENCY must be > 0"

        logger.info(
            """
Initiate %s loop:
    NAME: %s
    CONCURRENCY: %s
    SERVER_CONFIG: %s""",
            self.__clz_name,
            self.NAME,
            self.CONCURRENCY,
            self.SERVER_CONFIG,
        )

        self._concurrency = self.CONCURRENCY
        self._loop = asyncio.get_event_loop()

        self._server_config = parse_server_config(self.SERVER_CONFIG)
        self._server = Server(self.NAME, self._server_config, loop=self._loop)
        self.__ctrl_queue = make_ctrl_queue(self.CONCURRENCY, loop=self._loop)

        # Running task ids cache
        self._task_ids = set()

        self._stop = False

    @property
    def __clz_name(self):
        return self.__class__.__name__

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, val):
        self._stop = val

    @property
    def concurrency(self):
        return self._concurrency

    @concurrency.setter
    def concurrency(self, concurrency):
        self._concurrency = concurrency
        self.__ctrl_queue = make_ctrl_queue(concurrency, loop=self._loop)

    def _create_task(self, task, task_type=None):
        """Wrap `loop.create_task`
        We add an id to task if `task_id` is not None
        """

        future = self._loop.create_task(task)
        future.ch_name = self.NAME
        future.ch_type = task_type
        return future

    def _cache_task_id(self, task_id):
        """Cache running tasks' ids"""
        self._task_ids.add(task_id)

    def _uncache_task_id(self, task_id):
        """Remove running tasks' ids from cache"""
        try:
            self._task_ids.remove(task_id)
        except KeyError:
            pass

    async def make_task(self, task_id, task):
        """This function is the procedure of a task.

        The function must be implemented for handling every tasks
        """

        logger.error("%s: make_task is not implemented", self.__clz_name)
        raise NotImplementedError("ChihuoLoop.make_task must be implemented")

    async def next_task(self):
        resp = await self._server.pop_left()
        value = resp.value()
        if not value:
            return None, None

        task_id, raw_task = value
        task = stdjson.loads(raw_task)
        return task_id, task

    async def _task_loop(self):
        """Main loop"""

        while True:
            # Stop the loop
            if self._stop:
                logger.debug("%s: task_loop stop", self.__clz_name)
                return

            await self.__ctrl_queue.get()

            if self._stop:
                logger.debug("%s: task_loop stop", self.__clz_name)
                return

            task_id, task = await self.next_task()
            if task_id is None and task is None:
                await self.sleep(1)
                # Release the task
                await self.release()
                continue

            future = self._create_task(
                self._wrap_task(task_id, task), task_type=ChihuoType.Task
            )
            self._cache_task_id(task_id)
            future.add_done_callback(lambda _: self._uncache_task_id(task_id))
            future.ch_task = (task_id, task)

    async def _wrap_task(self, task_id, task):
        """Wrap task
        Handle `asyncio.CancelledError`

        If the task fails, adding task back to backend
        """

        try:
            await self.make_task(task_id, task)
        except asyncio.CancelledError:
            await self.add_task((task_id, task), direction=Direction.Reverse)
            logger.error("task fail: %s: CancelledError: %s", self.__clz_name, task)
        except Exception as err:
            await self.add_task((task_id, task), direction=Direction.Reverse)
            logger.error(
                "task fail: %s, task_id: %s, task: %s, error: %s, traceback: %s",
                self.__clz_name,
                task_id,
                task,
                err,
                traceback.format_exc(),
            )  # yapf: disable

    async def add_task(
        self, *pairs, finished=True, ignore_running=False, direction=Direction.Forward
    ):
        """Add a task to backend server

        `pairs`: [(task_id1, task1), (task_id2, task2), ...]
            `pairs` are the information of tasks.

        `task_id`: str or bytes
            `task_id` is the unique identification for a task.
        `task`: object
            `task` is the information that can be dumped as json about the task.

        `finished`: bool
            if finished is true, we add the task only if the task is not finished.
            Else, we add the task whether or not the task is finished.
        `ignore_running`: bool
            if ignore_running is true, the task will be added to the task queue
            only if there is not a task which is running with same task_id
        `direction`: chihuo.Direction
            if direction is `Direction.Forward`, the task will be appended to the
            tail of queue, received at last. if direction is `Direction.Reverse`, the
            task will be appended to the head of queue, received at first.
        """

        if ignore_running:
            # Remove these tasks which is running
            pairs = [pair for pair in pairs if pair[0] not in self._task_ids]

        if finished:
            unfinished_pairs = []
            for (task_id, task) in pairs:
                resp = await self._server.finished(task_id)
                if not resp.value():
                    unfinished_pairs.append((task_id, task))
            pairs = unfinished_pairs

        if not pairs:
            return

        # Serialize tasks
        pairs = [(task_id, serialize_json(task)) for task_id, task in pairs]

        if direction == Direction.Forward:
            await self._server.pushnx(*pairs)
        else:
            await self._server.pushnx_left(*pairs)

    async def task_finish(self, task_id):
        logger.info("%s: task_finish: %s", self.__clz_name, task_id)

        await self._server.finish(task_id)

    async def task_unfinish(self, task_id):
        logger.info("%s: task_unfinish: %s", self.__clz_name, task_id)

        await self._server.unfinish(task_id)

    async def release(self):
        # If ctrl_queue is not full, we put a chance to it.
        # When self._stop_task_loop is fired, ctrl_queue can be full.
        if not self.__ctrl_queue.full():
            await self.__ctrl_queue.put(1)

    def length(self):
        """How many tasks are there"""

        return self._concurrency - self.__ctrl_queue.qsize()

    async def sleep(self, second):
        await asyncio.sleep(second, loop=self._loop)

    def _sendback_and_cancel_tasks(self):
        logger.info("%s: sendback and cancel tasks", self.__clz_name)

        pairs = []
        tasks = asyncio.all_tasks(self._loop)
        for task in tasks:
            if (
                getattr(task, "ch_name", None) == self.NAME
                and task.ch_type == ChihuoType.Task
            ):
                # Remove cached tasks' id
                # Here, tasks' id are in cache, we need to remove them out cache,
                # then, send back tasks to backend
                self._uncache_task_id(task.ch_task[0])

                pairs.append(task.ch_task)
                task.cancel()

        if not pairs:
            logger.info("%s: No find tasks", self.__clz_name)
            return

        self._create_task(self._sendback_tasks(pairs), task_type=ChihuoType.SendBack)

    async def _sendback_tasks(self, pairs):
        logger.info("%s: sendback tasks", self.__clz_name)
        logger.info("%s: sendback_task: tasks: %s", self.__clz_name, pairs)

        await self.add_task(*pairs, direction=Direction.Reverse)

        logger.info("%s: sendback_task has done", self.__clz_name)

    def _run(self):
        logger.info("%s: run", self.__clz_name)

        if hasattr(self, "start") and isinstance(self.start, types.MethodType):
            self._create_task(self.start(), task_type=ChihuoType.Start)

        self._create_task(self._task_loop(), task_type=ChihuoType.TaskLoop)
