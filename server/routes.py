from aiohttp.web import Application
from .views import index, push_to_queue
from .settings import STATIC_DIR


def setup_routes(app: Application):
    app.router.add_get('/', index)
    app.router.add_post('/', push_to_queue)

    app.router.add_static('/static', STATIC_DIR)
