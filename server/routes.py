from aiohttp.web import Application
from .views import index, add_file
from .settings import STATIC_DIR


def setup_routes(app: Application):
    app.router.add_get('/', index)
    app.router.add_post('/', add_file)

    app.router.add_static('/static', STATIC_DIR)
