import aiosqlite
import aioredis

from decryption import Decrypter, DecryptionTaskManager


def setup_startup_events(application):
    for event in _STARTUP_EVENTS:
        application.on_startup.append(event)


async def start_decrypter(application):
    redis_client = application['redis']
    db_client = application['database']
    task_manager = DecryptionTaskManager(db_client, redis_client)
    decrypter = Decrypter(task_manager)
    application['decrypter'] = decrypter
    application['task_manager'] = task_manager


async def start_sqlite(application):
    application['database'] = await aiosqlite.connect("decryption.sqlite3")


async def start_redis(application):
    redis_client = aioredis.Redis()
    application['redis'] = redis_client


_STARTUP_EVENTS = [
    start_sqlite,
    start_redis,
    start_decrypter,
]
