import aiosqlite
import aioredis
from aioredis.connection import ConnectionError

from decryption import Decrypter, DecryptionTaskManager
from decryption.db_clients import get_db_client


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
    db_conn = await aiosqlite.connect("decryption.sqlite3")
    await db_conn.execute(
        "CREATE TABLE IF NOT EXISTS main.tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, file_path TEXT, status INTEGER)"
    )
    application['database'] = get_db_client(db_conn)


async def start_redis(application):
    redis_client = aioredis.Redis()
    redis_conn = redis_client.connection_pool.make_connection()

    try:
        await redis_conn.connect()
    except BaseException:
        await redis_client.connection_pool.release(redis_conn)
        raise ConnectionError("Redis server is not available")

    application['redis'] = redis_client


_STARTUP_EVENTS = [
    start_sqlite,
    start_redis,
    start_decrypter,
]
