import sys
import pathlib
import aiounittest
import aioredis
import unittest

sys.path.append(str(pathlib.Path(__file__).parent.parent))
from application.queue import RedisQueue


class TestRedisQueue(aiounittest.AsyncTestCase):
    _queue_key = 'test_queue'

    def setUp(self):
        redis_client = aioredis.Redis()
        self.__redis_queue = RedisQueue(redis_client, self._queue_key)

    async def test_push_task_id(self):
        await self.__redis_queue.clear()
        task_id = "1234"
        await self.__redis_queue.push_task_id(task_id)
        pushed_task_id = await self.__redis_queue.get_next_task_id()
        await self.__redis_queue.clear()

        self.assertEqual(task_id, pushed_task_id)

    async def test_get_next_task_id(self):
        await self.__redis_queue.clear()
        next_task_id = await self.__redis_queue.get_next_task_id()
        self.assertIsNone(next_task_id)
        
        task_id_list = ["123", "456", "789"]
        
        for task_id in task_id_list:
            await self.__redis_queue.push_task_id(task_id)

        next_task_id = await self.__redis_queue.get_next_task_id()
        await self.__redis_queue.clear()
        
        self.assertEqual(next_task_id, task_id_list[0])


if __name__ == "__main__":
    unittest.main()
