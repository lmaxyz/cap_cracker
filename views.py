from aiohttp import web
import aiohttp_jinja2

from services import add_file_to_decryption_queue


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {'queue': []}


async def add_file(request: web.Request):
    post = await request.post()
    file = post.get("cap_file")
    file_name = file.filename

    if not file_name.endswith(".cap") and not file_name.endswith(".pcap"):
        return web.Response(text="Wrong file format", status=400)

    print(file)
    await add_file_to_decryption_queue(file.file, file.filename)
    return web.Response(text="OK")
