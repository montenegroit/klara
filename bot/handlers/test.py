from aiogram import Router
from aiogram.types import Message

test_router = Router(name=__name__)


@test_router.message()
async def message_handler(message: Message):
    await message.answer("Hello from test router!")
