import logging
import os

import aiohttp

from arithmetic import main_app

# Enable debug mode for asyncio
os.environ["PYTHONASYNCIODEBUG"] = "1"

app = main_app()


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    logging.getLogger("asyncio").setLevel(logging.DEBUG)
    aiohttp.web.run_app(app, )