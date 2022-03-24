import aiosqlite

from decryption import Decrypter


def setup_startup_events(application):
    for event in _STARTUP_EVENTS:
        application.on_startup.append(event)


async def run_decrypter(application):
    decrypter = Decrypter(None)
    await decrypter.run()
    application['decrypter'] = decrypter


async def start_sqlite(application):
    application['database'] = await aiosqlite.connect("decryption.sqlite3")


_STARTUP_EVENTS = [
    run_decrypter,
    start_sqlite
]
