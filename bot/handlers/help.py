import logging
from aiogram import Router, types
from bot.services.releases import get_last_release_version

logger = logging.getLogger(__name__)
router = Router()

_message = """
Вот список моих команд:
  /help - Получить данное сообщение
  
Список команд для супер админа:
  !ro - Дать бан
  
Список команд для донатеров:
  - пока не придумала, пишите Пахану @i63phc
  
"""


@router.message(commands="help")
async def test_admin_message(message: types.Message):
    print(message)

    version = await get_last_release_version()
    await message.answer(_message + f"<i><a href='#'>{version}</a></i>")

    # https://github.com/montenegroit/klara
