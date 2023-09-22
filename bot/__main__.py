import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from bot.config import config
from bot.handlers.test import test_router
from bot.handlers.banofbot import router as new_ban_router
from bot.handlers.bans import router as ban_router
from bot.handlers.help import router as help_router
from bot.handlers.reminder import router as reminder_router
from bot.handlers.replicate import router as prompt_router
from bot.handlers.weather import router as weather_router
from bot.middlewares.db import DbSessionMiddleware
from bot.middlewares.increase_message_count import IncreaseCountUserMessagesMiddleware


async def main():
    # Logging to stdout
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Creating DB engine for PostgreSQL
    engine = create_async_engine(str(config.postgres_dsn), future=True, echo=False)

    # Creating DB connections pool
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Creating bot and its dispatcher
    bot = Bot(token=config.bot_token, parse_mode="HTML")
    if config.custom_bot_api:
        bot.session.api = TelegramAPIServer.from_base(
            config.custom_bot_api, is_local=True
        )

    # Choosing FSM storage
    if config.bot_fsm_storage == "memory":
        dp = Dispatcher(storage=MemoryStorage())
    else:
        dp = Dispatcher(storage=RedisStorage.from_url(config.redis_dsn))

    # # Allow interaction in private chats (not groups or channels) only
    dp.message.filter(F.chat.type.in_({"group", "supergroup", "private"}))

    # Register middlewares
    # dp.message.middleware(DbSessionMiddleware(db_pool))
    # dp.message.middleware(IncreaseCountUserMessagesMiddleware())
    # dp.callback_query.middleware(DbSessionMiddleware(db_pool))

    # Routing
    # dp.include_router(test_router)

    # dp.include_router(ban_router)
    # dp.include_router(prompt_router)
    dp.include_router(help_router)
    # dp.include_router(reminder_router)
    dp.include_router(weather_router)
    # dp.include_router(new_ban_router)

    # Start
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    print("Start bot...")
    asyncio.run(main())
