from aiohttp import web
import aiohttp_jinja2

from .services import add_file_to_decryption_queue


ALLOWED_EXTENSIONS = [
    "cap", "pcap", "hccapx"
]

@aiohttp_jinja2.template('index.html')
async def index(request):
    task_manager = request.app['task_manager']
    all_tasks = await task_manager.get_task_list()

    return {'tasks': all_tasks}


async def push_to_queue(request: web.Request):
    post = await request.post()
    file = post.get("cap_file")

    file_ext = file.filename.split(".")[-1]

    
    if file_ext not in ALLOWED_EXTENSIONS:
        return web.Response(text="Wrong file format", status=400)

    task_manager = request.app['task_manager']
    await add_file_to_decryption_queue(file, task_manager)

    raise web.HTTPFound('/')

