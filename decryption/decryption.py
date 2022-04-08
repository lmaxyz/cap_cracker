from asyncio import get_event_loop, sleep
from concurrent.futures import ProcessPoolExecutor
from .queue import RedisQueue


class DecryptionTaskManager:
    def __init__(self, db_connection, redis_client):
        self._db_connection = db_connection
        self._redis_queue = RedisQueue(redis_client, "decryption_queue")

    async def get_unhandled_task(self):
        return await self._redis_queue.get_next_task_id()

    async def push_new_task(self, file_path):
        task_id = await self.__add_task_to_database(file_path)
        
        try:
            await self._redis_queue.push_task_id(task_id)
        except:
            await self.set_task_status(task_id, "failed")

    async def handle_task(self, task_id):
        pass

    async def set_task_status(self, task_id, status, status_msg=None):
        pass
    
    async def __add_task_to_database(self, file_path) -> int:
        return 1


class Decrypter:
    def __init__(self, task_manager: DecryptionTaskManager):
        self._event_loop = get_event_loop()
        self._task_manager = task_manager
        self._executor = ProcessPoolExecutor(max_workers=2)
        self._decryption_task = self._event_loop.create_task(self._run_decryption_loop())

    async def _run_decryption_loop(self):
        while True:
            if (file_path := await self._task_manager.get_unhandled_task()) is not None:
                print(file_path)
                # await self._event_loop.run_in_executor(self._executor, self._decrypt, (file_path,))
            print("Here")

            if self._event_loop.is_closed():
                print('broken')
                break

            await sleep(5)

    async def stop(self):
        if self._decryption_task is not None and not self._decryption_task.cancelled():
            self._decryption_task.cancel()

    def _decrypt(self, file_path):
        print(f"Decrypt file {file_path}")
        # self._task_manager.handle_task(file_path)
