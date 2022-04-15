import asyncio
import dataclasses

from asyncio import get_event_loop, sleep, Task
from asyncio.subprocess import create_subprocess_shell, PIPE
from concurrent.futures import ProcessPoolExecutor

from .queue import RedisQueue
from .db_clients import SQLiteClient
from .task import TaskStatus, DecryptionTask
from server.settings import CAP_FILES_STORAGE


class DecryptionTaskManager:
    def __init__(self, db_client, redis_client):
        self._db_client: SQLiteClient = db_client
        self._redis_queue = RedisQueue(redis_client, "decryption_queue")

    async def get_next_task(self):
        task_id = await self._redis_queue.get_next_task_id()

        if task_id is None:
            return None

        task = await self._db_client.get_task(task_id)
        return task

    async def push_new_task(self, file_path):
        task_id = await self.__add_task_to_database(file_path)
        
        try:
            await self._redis_queue.push_task_id(task_id)
        except Exception:
            await self.set_task_status(task_id, TaskStatus.FAILED)

    async def set_task_status(self, task_id: int, status: TaskStatus, status_msg=None):
        await self._db_client.change_task_status(task_id, status, status_msg)
    
    async def __add_task_to_database(self, file_path) -> int:
        return await self._db_client.add_task(file_path)

    async def get_task_list(self):
        return await self._db_client.get_all_tasks()


class Decrypter:
    def __init__(self, task_manager: DecryptionTaskManager):
        self._event_loop = get_event_loop()
        self._task_manager = task_manager
        self._executor = ProcessPoolExecutor(max_workers=2)
        self._decryption_task = self._event_loop.create_task(self._run_decryption_loop())
        self._running_tasks: list[Task] = []

    async def _run_decryption_loop(self):
        while True:
            try:
                await self._check_running_tasks()
                if len(self._running_tasks) < 2 and (task := await self._task_manager.get_next_task()) is not None:
                    print(task.file_name)
                    await self._task_manager.set_task_status(task.task_id, TaskStatus.PROCESSING)
                    self._running_tasks.append(self._event_loop.create_task(self._run_john(task)))

                print("Here")

                await sleep(3)
            except asyncio.CancelledError:
                print('exit task')
                self._running_tasks = []
                break
            except Exception as e:
                for task in self._running_tasks:
                    task.cancel()

                self._running_tasks = []

                context = {'message': 'Error with decryption process',
                           'exception': e,
                           'task': self._decryption_task}
                self._event_loop.call_exception_handler(context)
                
                break

    async def _check_running_tasks(self):
        for task in self._running_tasks:
            if not task.done():
                continue

            result: DecryptionTask = task.result()

            await self._task_manager.set_task_status(result.task_id, result.status, result.status_msg)

            self._running_tasks.remove(task)


    async def _handle_done_task(self, task):
        await self._task_manager.set_task_status(task.task_id, TaskStatus.FINISHED)

    async def _run_john(self, task: DecryptionTask) -> DecryptionTask:
        path_to_file = CAP_FILES_STORAGE / task.file_name
        # process = await create_subprocess_shell(f'john -w=/home/lmaxyz/Downloads/rockyou.txt --format=wpapsk {task.file_name}', stdout=PIPE, stderr=PIPE)
        process = await create_subprocess_shell(f'aircrack-ng {task.file_name} -e test -w ~/Downloads/Pass.txt -q', stdout=PIPE, stderr=PIPE)
        await sleep(5)
        stdout, stderr = await process.communicate()
        if stdout:
            task.status = TaskStatus.FINISHED
            task.status_msg = f'[stdout]\n{stdout.decode()}'
            # ToDo: parse john response
            
        if stderr:
            task.status = TaskStatus.FAILED
            task.status_msg = f'[stderr]\n{stderr.decode()}'

        return task
        

    async def stop(self):
        if self._decryption_task is not None and not self._decryption_task.cancelled():
            self._decryption_task.cancel()

    def _decrypt(self, task: DecryptionTask):
        print(f"Decrypt file {task.file_name}")
        # await self._task_manager.set_task_status(task.task_id, TaskStatus.FINISHED)
        # self._task_manager.handle_task(file_path)
