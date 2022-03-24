from asyncio import get_event_loop, sleep, ProactorEventLoop
from concurrent.futures import ProcessPoolExecutor


class Decrypter:
    def __init__(self, db_connection):
        self._event_loop = get_event_loop()
        self._task_manager = DecryptionTaskManager(db_connection)
        self._executor = ProcessPoolExecutor(max_workers=2)
        self._decryption_task = None

    async def run(self):
        self._decryption_task = self._event_loop.create_task(self._run_decryption_loop())

    async def _run_decryption_loop(self):
        while True:
            if await self._task_manager.has_unhandled_tasks():
                file_path = await self._task_manager.get_unhandled_task()
                # await self._event_loop.run_in_executor(self._executor, self._decrypt, (file_path,))
            print("Here")

            if self._event_loop.is_closed():
                print('breaked')
                break

            await sleep(5)

    async def stop(self):
        if self._decryption_task is not None and not self._decryption_task.cancelled():
            self._decryption_task.cancel()

        await self._decryption_task
        self._event_loop.stop()
        self._event_loop.close()

    def _decrypt(self, file_path):
        print(f"Decrypt file {file_path}")
        # self._task_manager.handle_task(file_path)


class DecryptionTaskManager:
    def __init__(self, db_connection):
        self._db_connection = db_connection

    async def has_unhandled_tasks(self):
        return True

    async def get_unhandled_task(self):
        return None

    async def push_new_task(self, file_path):
        pass

    async def handle_task(self, task_id):
        pass

    async def set_task_status(self, task_id, status):
        pass
