import aiohttp
from aiohttp import web
from config import DB_SETTINGS
from app.app import create_app

app = create_app(config=DB_SETTINGS)

if __name__ == '__main__':
    aiohttp.web.run_app(app)
