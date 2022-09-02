import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.telegram import TelegramAPIServer
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from magic_filter import F
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from bot.config import config
from bot.handlers.start import router as handlers_router
from bot.middlewares.db import DbSessionMiddleware


async def main():
    # Logging to stdout
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Creating DB engine for PostgreSQL
    engine = create_async_engine(config.postgres_dsn, future=True, echo=False)

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

    # Allow interaction in private chats (not groups or channels) only
    dp.message.filter(F.chat.type.in_({"group", "supergroup", "private"}))

    # Register middlewares
    dp.message.middleware(DbSessionMiddleware(db_pool))
    dp.callback_query.middleware(DbSessionMiddleware(db_pool))

    # Routing
    dp.include_router(handlers_router)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
