import asyncio
import aiohttp_jinja2
import jinja2

from aiohttp import web

from .settings import BASE_DIR
from .cleanup_events import setup_cleanup_events
from .startup_events import setup_startup_events
from .routes import setup_routes


async def _run_app(app):
    runner = web.AppRunner(app)
    await runner.setup()

    try:
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()

        while True:
            await asyncio.sleep(3600)
    finally:
        print('Cleanup...')
        await runner.cleanup()


def _create_application():
    app = web.Application()
    setup_startup_events(app)
    setup_cleanup_events(app)
    setup_routes(app)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(BASE_DIR/'templates'))

    return app


def start_app():
    app = _create_application()
    web.run_app(app)

    # app_task = loop.create_task(_run_app(app))
    # try:
    #     loop.run_until_complete(app_task)
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     app_task.cancel()
    #     asyncio.gather(app_task)
    #     loop.run_until_complete(loop.shutdown_asyncgens())
    #     loop.close()
