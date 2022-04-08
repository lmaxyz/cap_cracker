from aiohttp import web
import aiohttp_jinja2

from .services import add_file_to_decryption_queue


@aiohttp_jinja2.template('index.html')
async def index(request):
    task_manager = request.app['task_manager']
    all_tasks = await task_manager.get_task_list()

    return {'queue': all_tasks}


async def add_file(request: web.Request):
    post = await request.post()
    file = post.get("cap_file")
    file_name = file.filename

    if not file_name.endswith(".cap") and not file_name.endswith(".pcap"):
        return web.Response(text="Wrong file format", status=400)

    task_manager = request.app['task_manager']
    await add_file_to_decryption_queue(file, task_manager)

    return web.Response(text="OK")
