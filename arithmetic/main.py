from aiohttp import web
import jinja2
import aiohttp_jinja2
from .routes import setup_routes
from .middlewares import setup_middlewares


async def main_app():
    app = web.Application()
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('arithmetic', 'templates')
    )
    setup_routes(app)
    setup_middlewares(app)
    return app