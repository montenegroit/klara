import logging
from aiogram import Router, types
from aiogram.filters import Command
from bot.services.releases import get_last_release_version

logger = logging.getLogger(__name__)
router = Router(name=__name__)

_message = """
Вот список моих команд:
  /help - Получить данное сообщение
  
Список команд для супер админа:
  !ro - Дать бан
  
Список команд для донатеров:
  /prompt описание на англ - генератор изображения по тексту со stable diffusion

"""


@router.message(Command(commands="help"))  # Command(commands="help")
async def test_admin_message(message: types.Message):
    version = await get_last_release_version()
    await message.answer(_message + f"<i><a href='#'>{version}</a></i>")
