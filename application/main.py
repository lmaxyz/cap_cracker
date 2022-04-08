import sys
import asyncio
import aiohttp_jinja2
import jinja2

from aiohttp import web

from settings import BASE_DIR
sys.path.append(str(BASE_DIR))

from application.cleanup_events import setup_cleanup_events
from application.startup_events import setup_startup_events

from application.routes import setup_routes


async def main(app):
    runner = web.AppRunner(app)
    await runner.setup()

    try:
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()

        while True:
            await asyncio.sleep(3600)
    finally:
        await runner.cleanup()


def create_application():
    app = web.Application()
    setup_startup_events(app)
    setup_cleanup_events(app)
    setup_routes(app)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(BASE_DIR/'templates'))

    return app


if __name__ == "__main__":
    app = create_application()
    try:
        asyncio.run(main(app))
    except KeyboardInterrupt:
        pass
