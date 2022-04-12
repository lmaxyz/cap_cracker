

class RedisQueue:
    __queue_key = 'queue'

    def __init__(self, redis_client, queue_key: str = None, clean_if_exist: bool = False):
        self.__redis_client = redis_client
        
        if queue_key is not None:
            self.__queue_key = queue_key

        if clean_if_exist:
            self.clear()

    async def push_task_id(self, task_id):
        await self.__redis_client.lpush(self.__queue_key, task_id)

    async def get_next_task_id(self):
        task_id = await self.__redis_client.rpop(self.__queue_key)
        
        if task_id is not None:
            task_id = int(task_id.decode())

        return task_id

    async def task_is_in_queue(self, task_id) -> bool:
        return await self.__redis_client.lpos(self.__queue_key, task_id) is not None

    async def clear(self):
        await self.__redis_client.delete(self.__queue_key)
