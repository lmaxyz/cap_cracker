from aiohttp.web import Application
from .views import index, add_file


def setup_routes(app: Application):
    app.router.add_get('/', index)
    app.router.add_post('/', add_file)
