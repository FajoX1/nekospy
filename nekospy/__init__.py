from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from redis.asyncio import Redis

from nekospy import db, config

import asyncio

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    )
)
dp = Dispatcher()

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=(
        config.REDIS_PASSWORD 
        if config.REDIS_PASSWORD else None
    ),
)

asyncio.run(db.init_db())