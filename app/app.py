from aiohttp import web

import asyncpg

from .routes import setup_routes
from utils.logger import LogDispatcher

logger = LogDispatcher().log


async def create_app(config: dict):
    """Функция для генерации параметров приложения"""
    app = web.Application()
    app['config'] = config

    setup_routes(app)
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_shutdown)
    return app


async def on_start(app):
    """Функция создания соединения с БД"""
    config = app['config']
    try:
        app['db'] = await asyncpg.create_pool(database=config['db'],
                                              port=config['port'],
                                              user=config['user'],
                                              password=config['password'],
                                              host=config['host'])
        logger.info('Получено соединение с БД')
    except Exception as e:
        logger.info(f'Ошибка соединения с БД: {e}')


async def on_shutdown(app):
    """Функция закрытия соединения с БД"""
    await app['db'].close()
