

def setup_cleanup_events(app):
    for event in _CLEANUP_EVENTS:
        app.on_cleanup.append(event)


async def close_sqlite(app):
    await app['database'].close()


async def stop_decrypter(app):
    await app['decrypter'].stop()


async def stop_redis(app):
    await app['redis'].close()


_CLEANUP_EVENTS = [
    close_sqlite,
    stop_decrypter,
    stop_redis,
]
