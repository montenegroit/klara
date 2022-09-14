from tracemalloc import BaseFilter
from aiogram import types

from bot.config import config


class IsSuperAdmin(BaseFilter):
    async def __call__(self, message: types.Message, *args, **kwargs) -> bool:
        if message.from_user.id == config.super_admin_id:
            return True
        return False
