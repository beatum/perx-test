import time

from aiohttp_jinja2 import template
from .back import get_data
from ..constants import use_print


@template('index.html')
async def index(request):
    start_time = time.monotonic()
    items = await get_data()
    stop_time = time.monotonic() - start_time
    stop_time = round(stop_time, 3)
    if use_print:
        print(f'{stop_time}')
    return {'items': items, 'total_time': stop_time}
