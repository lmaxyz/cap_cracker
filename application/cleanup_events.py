

def setup_cleanup_events(application):
    for event in _CLEANUP_EVENTS:
        application.on_cleanup.append(event)


async def close_sqlite(application):
    await application['database'].close()


async def stop_decrypter(application):
    await application['decrypter'].stop()


_CLEANUP_EVENTS = [
    close_sqlite,
    stop_decrypter,
]
